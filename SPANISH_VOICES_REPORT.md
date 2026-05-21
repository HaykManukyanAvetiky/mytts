# Spanish Voices Test Report

## Summary

Tested all Spanish voices that failed to generate preview files (0-byte files).

**Result: ALL 32 failed voices are permanently unavailable in Edge TTS.**

## Test Results

### Failed Voices (32 total) - MUST BE REMOVED

These voices do NOT exist in Edge TTS and will always fail:

#### Spain (es-ES) - 17 voices
- es-ES-AbrilNeural
- es-ES-ArabellaMultilingualNeural
- es-ES-ArnauNeural
- es-ES-DarioNeural
- es-ES-EliasNeural
- es-ES-EstrellaNeural
- es-ES-IreneNeural
- es-ES-IsidoraMultilingualNeural
- es-ES-LaiaNeural
- es-ES-LiaNeural
- es-ES-NilNeural
- es-ES-SaulNeural
- es-ES-TeoNeural
- es-ES-TrianaNeural
- es-ES-TristanMultilingualNeural
- es-ES-VeraNeural
- es-ES-XimenaMultilingualNeural

#### Mexico (es-MX) - 15 voices
- es-MX-BeatrizNeural
- es-MX-CandelaNeural
- es-MX-CarlotaNeural
- es-MX-CecilioNeural
- es-MX-DaliaMultilingualNeural
- es-MX-GerardoNeural
- es-MX-JorgeMultilingualNeural
- es-MX-LarissaNeural
- es-MX-LibertoNeural
- es-MX-LucianoNeural
- es-MX-MarinaNeural
- es-MX-NuriaNeural
- es-MX-PelayoNeural
- es-MX-RenataNeural
- es-MX-YagoNeural

### Working Voices (45 total) - KEEP IN CONFIG

These voices ARE available and working correctly:

#### Argentina (es-AR) - 2 voices
- es-AR-ElenaNeural ✓
- es-AR-TomasNeural ✓

#### Bolivia (es-BO) - 2 voices
- es-BO-MarceloNeural ✓
- es-BO-SofiaNeural ✓

#### Chile (es-CL) - 2 voices
- es-CL-CatalinaNeural ✓
- es-CL-LorenzoNeural ✓

#### Colombia (es-CO) - 2 voices
- es-CO-GonzaloNeural ✓
- es-CO-SalomeNeural ✓

#### Costa Rica (es-CR) - 2 voices
- es-CR-JuanNeural ✓
- es-CR-MariaNeural ✓

#### Cuba (es-CU) - 2 voices
- es-CU-BelkysNeural ✓
- es-CU-ManuelNeural ✓

#### Dominican Republic (es-DO) - 2 voices
- es-DO-EmilioNeural ✓
- es-DO-RamonaNeural ✓

#### Ecuador (es-EC) - 2 voices
- es-EC-AndreaNeural ✓
- es-EC-LuisNeural ✓

#### Spain (es-ES) - 3 voices ONLY
- es-ES-AlvaroNeural ✓
- es-ES-ElviraNeural ✓
- es-ES-XimenaNeural ✓

#### Equatorial Guinea (es-GQ) - 2 voices
- es-GQ-JavierNeural ✓
- es-GQ-TeresaNeural ✓

#### Guatemala (es-GT) - 2 voices
- es-GT-AndresNeural ✓
- es-GT-MartaNeural ✓

#### Honduras (es-HN) - 2 voices
- es-HN-CarlosNeural ✓
- es-HN-KarlaNeural ✓

#### Mexico (es-MX) - 2 voices ONLY
- es-MX-DaliaNeural ✓
- es-MX-JorgeNeural ✓

#### Nicaragua (es-NI) - 2 voices
- es-NI-FedericoNeural ✓
- es-NI-YolandaNeural ✓

#### Panama (es-PA) - 2 voices
- es-PA-MargaritaNeural ✓
- es-PA-RobertoNeural ✓

#### Peru (es-PE) - 2 voices
- es-PE-AlexNeural ✓
- es-PE-CamilaNeural ✓

#### Puerto Rico (es-PR) - 2 voices
- es-PR-KarinaNeural ✓
- es-PR-VictorNeural ✓

#### Paraguay (es-PY) - 2 voices
- es-PY-MarioNeural ✓
- es-PY-TaniaNeural ✓

#### El Salvador (es-SV) - 2 voices
- es-SV-LorenaNeural ✓
- es-SV-RodrigoNeural ✓

#### United States (es-US) - 2 voices
- es-US-AlonsoNeural ✓
- es-US-PalomaNeural ✓

#### Uruguay (es-UY) - 2 voices
- es-UY-MateoNeural ✓
- es-UY-ValentinaNeural ✓

#### Venezuela (es-VE) - 2 voices
- es-VE-PaolaNeural ✓
- es-VE-SebastianNeural ✓

## Analysis

1. **Spain (es-ES)**: Only 3 out of 20 configured voices work (15% success rate)
2. **Mexico (es-MX)**: Only 2 out of 17 configured voices work (12% success rate)
3. **Other regions**: All voices work (100% success rate)

The config appears to have been created with outdated or incorrect voice lists for Spain and Mexico.

## Recommendation

Remove all 32 failed voices from `/Users/haykmanukyan/work/mytts/backend/config.py`.

This will:
- Prevent users from selecting non-existent voices
- Avoid confusing "No audio received" errors
- Clean up the voice selection UI
- Improve user experience

## Testing Method

All voices were tested using:
```python
edge_tts.Communicate(text="Hola, esta es una prueba de voz.", voice=voice_id)
```

Voices that returned `NoAudioReceived` exception are confirmed unavailable.
