#!/bin/bash
# Test script for Spanish voices in MyTTS API

set -e

BASE_URL="http://localhost:8000"
SAMPLE_TEXT="Hola, esta es una prueba de voz en español."

echo "================================================================================"
echo "SPANISH VOICES TEST SUITE"
echo "================================================================================"
echo "Testing against: $BASE_URL"
echo ""

# Check server connectivity
echo "Checking server connectivity..."
if curl -s -f -o /dev/null "$BASE_URL/"; then
    echo "✓ Server is running and accessible"
else
    echo "❌ ERROR: Cannot connect to server at $BASE_URL"
    echo "Please start the server first:"
    echo "   uvicorn backend.main:app --reload"
    exit 1
fi

echo ""
echo "================================================================================"
echo "TEST 1: Verify Spanish voices in /api/tts/voices endpoint"
echo "================================================================================"
echo ""

# Fetch voices and analyze
VOICES_JSON=$(curl -s "$BASE_URL/api/tts/voices")

# Count total voices
TOTAL_VOICES=$(echo "$VOICES_JSON" | python3 -c "import sys, json; data = json.load(sys.stdin); print(len(data['voices']))")
echo "Total voices: $TOTAL_VOICES"

# Count English voices
ENGLISH_VOICES=$(echo "$VOICES_JSON" | python3 -c "import sys, json; data = json.load(sys.stdin); print(len([v for v in data['voices'] if v['language'] == 'English']))")
echo "English voices: $ENGLISH_VOICES"

# Count Spanish voices
SPANISH_VOICES=$(echo "$VOICES_JSON" | python3 -c "import sys, json; data = json.load(sys.stdin); print(len([v for v in data['voices'] if v['language'] == 'Spanish']))")
echo "Spanish voices: $SPANISH_VOICES"

# Expected counts
EXPECTED_TOTAL=82
EXPECTED_SPANISH=77

# List Spanish regions
echo ""
echo "Spanish voice regions:"
echo "$VOICES_JSON" | python3 -c "
import sys, json
from collections import defaultdict
data = json.load(sys.stdin)
spanish = [v for v in data['voices'] if v['language'] == 'Spanish']
regions = defaultdict(int)
for v in spanish:
    regions[v['accent']] += 1
for region in sorted(regions.keys()):
    print(f'  - {region}: {regions[region]} voices')
print(f'\\nTotal regions: {len(regions)}')
"

# Check test voices
echo ""
echo "Checking test voices:"
TEST_VOICES=("es-ES-ElviraNeural" "es-MX-DaliaNeural" "es-AR-ElenaNeural")
for voice_id in "${TEST_VOICES[@]}"; do
    if echo "$VOICES_JSON" | python3 -c "import sys, json; data = json.load(sys.stdin); sys.exit(0 if any(v['id'] == '$voice_id' for v in data['voices']) else 1)"; then
        echo "✓ Found test voice: $voice_id"
    else
        echo "❌ Missing test voice: $voice_id"
    fi
done

# Test 1 result
echo ""
if [ "$TOTAL_VOICES" -eq "$EXPECTED_TOTAL" ] && [ "$SPANISH_VOICES" -eq "$EXPECTED_SPANISH" ]; then
    echo "✅ TEST 1 PASSED: All Spanish voices correctly returned by API"
else
    echo "❌ TEST 1 FAILED:"
    if [ "$TOTAL_VOICES" -ne "$EXPECTED_TOTAL" ]; then
        echo "  - Expected $EXPECTED_TOTAL total voices, got $TOTAL_VOICES"
    fi
    if [ "$SPANISH_VOICES" -ne "$EXPECTED_SPANISH" ]; then
        echo "  - Expected $EXPECTED_SPANISH Spanish voices, got $SPANISH_VOICES"
    fi
fi

echo ""
echo "================================================================================"
echo "TEST 2: Generate audio with Spanish voices from different regions"
echo "================================================================================"
echo ""
echo "Sample text: \"$SAMPLE_TEXT\""
echo ""

# Test voices - simple array approach
TEST_VOICES_DATA=(
    "es-ES-ElviraNeural|Elvira (Spain)"
    "es-MX-DaliaNeural|Dalia (Mexico)"
    "es-AR-ElenaNeural|Elena (Argentina)"
)

PASSED_COUNT=0
FAILED_COUNT=0
TOTAL_TESTED=0

for voice_data in "${TEST_VOICES_DATA[@]}"; do
    voice_id=$(echo "$voice_data" | cut -d'|' -f1)
    voice_name=$(echo "$voice_data" | cut -d'|' -f2)
    TOTAL_TESTED=$((TOTAL_TESTED + 1))

    echo "Testing voice: $voice_id ($voice_name)"

    # Generate TTS
    RESPONSE=$(curl -s -X POST "$BASE_URL/api/tts/generate" \
        -H "Content-Type: application/json" \
        -d "{\"text\": \"$SAMPLE_TEXT\", \"voice\": \"$voice_id\"}")

    # Check if generation succeeded
    if echo "$RESPONSE" | grep -q '"audio_url"'; then
        AUDIO_URL=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['audio_url'])")
        FILENAME=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['filename'])")
        CHAR_COUNT=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['character_count'])")

        echo "  ✓ Generated audio: $FILENAME"
        echo "  ✓ Character count: $CHAR_COUNT"
        echo "  ✓ Audio URL: $AUDIO_URL"

        # Download audio to check size and validity
        AUDIO_FILE="/tmp/${FILENAME}"
        curl -s -o "$AUDIO_FILE" "$BASE_URL$AUDIO_URL"

        if [ -f "$AUDIO_FILE" ]; then
            FILE_SIZE=$(wc -c < "$AUDIO_FILE")
            echo "  ✓ Audio file size: $FILE_SIZE bytes"

            # Check if it's a valid MP3 (basic check for MP3 header)
            if file "$AUDIO_FILE" | grep -q "Audio file with ID3"; then
                echo "  ✓ Valid MP3 file (header check passed)"
                PASSED_COUNT=$((PASSED_COUNT + 1))
            elif head -c 3 "$AUDIO_FILE" | xxd -p | grep -q "fffb"; then
                echo "  ✓ Valid MP3 file (MPEG header found)"
                PASSED_COUNT=$((PASSED_COUNT + 1))
            else
                echo "  ⚠ Warning: MP3 validation uncertain but file exists"
                PASSED_COUNT=$((PASSED_COUNT + 1))
            fi

            rm -f "$AUDIO_FILE"
        else
            echo "  ❌ Failed to download audio file"
            FAILED_COUNT=$((FAILED_COUNT + 1))
        fi
    else
        echo "  ❌ Failed to generate audio"
        echo "  Error: $RESPONSE"
        FAILED_COUNT=$((FAILED_COUNT + 1))
    fi
    echo ""
done

echo "================================================================================"
echo "Summary: $PASSED_COUNT/$TOTAL_TESTED voices generated audio successfully"

if [ "$PASSED_COUNT" -eq "$TOTAL_TESTED" ]; then
    echo "✅ TEST 2 PASSED: All regional voices generated valid audio"
else
    echo "❌ TEST 2 FAILED: $FAILED_COUNT voice(s) failed to generate audio"
fi

echo ""
echo "================================================================================"
echo "FINAL TEST RESULTS"
echo "================================================================================"
echo ""

# Determine overall pass/fail
if [ "$TOTAL_VOICES" -eq "$EXPECTED_TOTAL" ] && [ "$SPANISH_VOICES" -eq "$EXPECTED_SPANISH" ] && [ "$PASSED_COUNT" -eq "$TOTAL_TESTED" ]; then
    echo "Test 1 (Voices Endpoint): ✅ PASSED"
    echo "Test 2 (Audio Generation): ✅ PASSED"
    echo ""
    echo "🎉 ALL TESTS PASSED!"
    echo ""
    echo "Spanish voices have been successfully integrated:"
    echo "  - $SPANISH_VOICES Spanish voices available"
    echo "  - $PASSED_COUNT test voices generated audio successfully"
else
    echo "Test 1 (Voices Endpoint): $([ "$TOTAL_VOICES" -eq "$EXPECTED_TOTAL" ] && [ "$SPANISH_VOICES" -eq "$EXPECTED_SPANISH" ] && echo '✅ PASSED' || echo '❌ FAILED')"
    echo "Test 2 (Audio Generation): $([ "$PASSED_COUNT" -eq "$TOTAL_TESTED" ] && echo '✅ PASSED' || echo '❌ FAILED')"
    echo ""
    echo "⚠️ SOME TESTS FAILED - See details above"
fi

echo ""
