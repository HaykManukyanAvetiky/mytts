#!/bin/bash

# Complete pitch control test for all new language voices
# Tests -20Hz, 0Hz, and +20Hz pitch adjustments
# Downloads actual audio files and verifies file sizes

BASE_URL="http://localhost:8000"
OUTPUT_DIR="/Users/haykmanukyan/work/mytts/test_pitch_output"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "================================================================================"
echo "PITCH CONTROL TEST SUITE (Complete)"
echo "================================================================================"
echo ""
echo "Testing 5 languages x 3 pitch values = 15 total tests"
echo ""

# Counters
TOTAL=0
PASSED=0
FAILED=0

# Test function
test_pitch() {
    local LANGUAGE=$1
    local VOICE=$2
    local TEXT=$3
    local PITCH_LABEL=$4
    local PITCH_VALUE=$5

    TOTAL=$((TOTAL + 1))

    # Create JSON payload
    JSON_PAYLOAD=$(cat <<EOF
{
  "text": "$TEXT",
  "voice": "$VOICE",
  "pitch": "$PITCH_VALUE"
}
EOF
)

    echo -n "  Testing pitch $PITCH_LABEL ($PITCH_VALUE)... "

    # Make request to generate endpoint
    RESPONSE=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$JSON_PAYLOAD" \
        "$BASE_URL/api/tts/generate")

    # Check if response contains audio_url
    if echo "$RESPONSE" | grep -q '"audio_url"'; then
        # Extract audio URL
        AUDIO_URL=$(echo "$RESPONSE" | grep -o '"audio_url":"[^"]*"' | cut -d'"' -f4)

        if [ -n "$AUDIO_URL" ]; then
            # Download the actual audio file
            FILENAME="${LANGUAGE}_${VOICE}_${PITCH_LABEL}.mp3"
            OUTPUT_PATH="$OUTPUT_DIR/$FILENAME"

            HTTP_CODE=$(curl -s -w "%{http_code}" -o "$OUTPUT_PATH" \
                "$BASE_URL$AUDIO_URL")

            if [ "$HTTP_CODE" = "200" ]; then
                # Get file size
                FILE_SIZE=$(stat -f%z "$OUTPUT_PATH" 2>/dev/null || stat -c%s "$OUTPUT_PATH" 2>/dev/null)

                if [ "$FILE_SIZE" -gt 1000 ]; then
                    FILE_SIZE_KB=$((FILE_SIZE / 1024))
                    echo "✓ SUCCESS (${FILE_SIZE_KB} KB)"
                    PASSED=$((PASSED + 1))
                else
                    echo "✗ FAILED - File too small (${FILE_SIZE} bytes)"
                    FAILED=$((FAILED + 1))
                fi
            else
                echo "✗ FAILED - HTTP $HTTP_CODE downloading audio"
                FAILED=$((FAILED + 1))
            fi
        else
            echo "✗ FAILED - No audio URL in response"
            FAILED=$((FAILED + 1))
        fi
    else
        echo "✗ FAILED - Invalid response: $RESPONSE"
        FAILED=$((FAILED + 1))
    fi
}

# Test English
echo ""
echo "English (en-US-GuyNeural):"
echo "--------------------------------------------------------------------------------"
test_pitch "English" "en-US-GuyNeural" "Testing pitch control with English voice." "-20Hz" "-20Hz"
test_pitch "English" "en-US-GuyNeural" "Testing pitch control with English voice." "0Hz" "+0Hz"
test_pitch "English" "en-US-GuyNeural" "Testing pitch control with English voice." "+20Hz" "+20Hz"

# Test Spanish
echo ""
echo "Spanish (es-AR-ElenaNeural):"
echo "--------------------------------------------------------------------------------"
test_pitch "Spanish" "es-AR-ElenaNeural" "Probando el control de tono con voz española." "-20Hz" "-20Hz"
test_pitch "Spanish" "es-AR-ElenaNeural" "Probando el control de tono con voz española." "0Hz" "+0Hz"
test_pitch "Spanish" "es-AR-ElenaNeural" "Probando el control de tono con voz española." "+20Hz" "+20Hz"

# Test French
echo ""
echo "French (fr-FR-DeniseNeural):"
echo "--------------------------------------------------------------------------------"
test_pitch "French" "fr-FR-DeniseNeural" "Test du contrôle de la hauteur avec une voix française." "-20Hz" "-20Hz"
test_pitch "French" "fr-FR-DeniseNeural" "Test du contrôle de la hauteur avec une voix française." "0Hz" "+0Hz"
test_pitch "French" "fr-FR-DeniseNeural" "Test du contrôle de la hauteur avec une voix française." "+20Hz" "+20Hz"

# Test German
echo ""
echo "German (de-DE-ConradNeural):"
echo "--------------------------------------------------------------------------------"
test_pitch "German" "de-DE-ConradNeural" "Testen der Tonhöhenregelung mit deutscher Stimme." "-20Hz" "-20Hz"
test_pitch "German" "de-DE-ConradNeural" "Testen der Tonhöhenregelung mit deutscher Stimme." "0Hz" "+0Hz"
test_pitch "German" "de-DE-ConradNeural" "Testen der Tonhöhenregelung mit deutscher Stimme." "+20Hz" "+20Hz"

# Test Portuguese
echo ""
echo "Portuguese (pt-BR-AntonioNeural):"
echo "--------------------------------------------------------------------------------"
test_pitch "Portuguese" "pt-BR-AntonioNeural" "Testando o controle de tom com voz portuguesa." "-20Hz" "-20Hz"
test_pitch "Portuguese" "pt-BR-AntonioNeural" "Testando o controle de tom com voz portuguesa." "0Hz" "+0Hz"
test_pitch "Portuguese" "pt-BR-AntonioNeural" "Testando o controle de tom com voz portuguesa." "+20Hz" "+20Hz"

# Print summary
echo ""
echo "================================================================================"
echo "TEST SUMMARY"
echo "================================================================================"
echo ""
echo "Total Tests: $TOTAL"
echo "Passed: $PASSED ✓"
echo "Failed: $FAILED ✗"

if [ $TOTAL -gt 0 ]; then
    SUCCESS_RATE=$((PASSED * 100 / TOTAL))
    echo "Success Rate: ${SUCCESS_RATE}%"
fi

echo ""
echo "--------------------------------------------------------------------------------"
echo "Results by Language:"
echo "--------------------------------------------------------------------------------"

# Count successful audio files per language
for LANG in "English" "Spanish" "French" "German" "Portuguese"; do
    LANG_COUNT=0
    for FILE in "$OUTPUT_DIR"/${LANG}_*.mp3; do
        if [ -f "$FILE" ]; then
            FILE_SIZE=$(stat -f%z "$FILE" 2>/dev/null || stat -c%s "$FILE" 2>/dev/null)
            if [ "$FILE_SIZE" -gt 1000 ]; then
                LANG_COUNT=$((LANG_COUNT + 1))
            fi
        fi
    done

    if [ "$LANG_COUNT" = "3" ]; then
        STATUS="✓ PASS"
    else
        STATUS="✗ FAIL"
    fi
    printf "%-12s: %s/3 %s\n" "$LANG" "$LANG_COUNT" "$STATUS"
done

echo ""
echo "--------------------------------------------------------------------------------"
echo "Audio files saved to: $OUTPUT_DIR"
echo "--------------------------------------------------------------------------------"

# List generated files with sizes
echo ""
echo "Generated files:"
for FILE in "$OUTPUT_DIR"/*.mp3; do
    if [ -f "$FILE" ]; then
        FILE_SIZE=$(stat -f%z "$FILE" 2>/dev/null || stat -c%s "$FILE" 2>/dev/null)
        FILE_SIZE_KB=$((FILE_SIZE / 1024))
        BASENAME=$(basename "$FILE")
        printf "  - %s (%d KB)\n" "$BASENAME" "$FILE_SIZE_KB"
    fi
done

if [ $FAILED -eq 0 ]; then
    echo ""
    echo "✓ ALL TESTS PASSED!"
    exit 0
else
    echo ""
    echo "✗ $FAILED TEST(S) FAILED"
    exit 1
fi
