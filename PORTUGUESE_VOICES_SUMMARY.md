# Portuguese Voices Discovery - Edge TTS

**Date:** 2025-12-18
**Total Portuguese Voices:** 5

## Overview

Edge TTS provides 5 Portuguese voices across 2 regional variants:
- **pt-BR (Brazilian Portuguese):** 3 voices (1 male, 2 female)
- **pt-PT (European Portuguese):** 2 voices (1 male, 1 female)

---

## Detailed Voice List

### Brazilian Portuguese (pt-BR)

#### 1. Antonio (Male)
- **Voice ID:** `pt-BR-AntonioNeural`
- **Full Name:** Microsoft Antonio Online (Natural) - Portuguese (Brazil)
- **Gender:** Male
- **Locale:** pt-BR
- **Region:** Brazil

#### 2. Francisca (Female)
- **Voice ID:** `pt-BR-FranciscaNeural`
- **Full Name:** Microsoft Francisca Online (Natural) - Portuguese (Brazil)
- **Gender:** Female
- **Locale:** pt-BR
- **Region:** Brazil

#### 3. Thalita Multilingual (Female)
- **Voice ID:** `pt-BR-ThalitaMultilingualNeural`
- **Full Name:** Microsoft ThalitaMultilingual Online (Natural) - Portuguese (Brazil)
- **Gender:** Female
- **Locale:** pt-BR
- **Region:** Brazil
- **Note:** Multilingual voice

---

### European Portuguese (pt-PT)

#### 4. Duarte (Male)
- **Voice ID:** `pt-PT-DuarteNeural`
- **Full Name:** Microsoft Duarte Online (Natural) - Portuguese (Portugal)
- **Gender:** Male
- **Locale:** pt-PT
- **Region:** Portugal

#### 5. Raquel (Female)
- **Voice ID:** `pt-PT-RaquelNeural`
- **Full Name:** Microsoft Raquel Online (Natural) - Portuguese (Portugal)
- **Gender:** Female
- **Locale:** pt-PT
- **Region:** Portugal

---

## VoiceInfo Entries for config.py

Below are the ready-to-use VoiceInfo entries that can be added to your config.py file:

```python
# Brazilian Portuguese (pt-BR) - 3 voices
VoiceInfo(id="pt-BR-AntonioNeural", name="Antonio", gender="Male", region="Brazil"),
VoiceInfo(id="pt-BR-FranciscaNeural", name="Francisca", gender="Female", region="Brazil"),
VoiceInfo(id="pt-BR-ThalitaMultilingualNeural", name="Thalita Multilingual", gender="Female", region="Brazil"),

# European Portuguese (pt-PT) - 2 voices
VoiceInfo(id="pt-PT-DuarteNeural", name="Duarte", gender="Male", region="Portugal"),
VoiceInfo(id="pt-PT-RaquelNeural", name="Raquel", gender="Female", region="Portugal"),
```

---

## Summary Statistics

| Region | Male Voices | Female Voices | Total |
|--------|-------------|---------------|-------|
| Brazil (pt-BR) | 1 | 2 | 3 |
| Portugal (pt-PT) | 1 | 1 | 2 |
| **Total** | **2** | **3** | **5** |

---

## Comparison with Other Languages

| Language | Total Voices |
|----------|--------------|
| Spanish | 77 |
| French | 13 |
| German | 10 |
| **Portuguese** | **5** |

---

## Technical Details

All Portuguese voices use:
- Neural TTS technology (indicated by "Neural" suffix)
- Suggested Codec: audio-24khz-48kbitrate-mono-mp3
- Status: GA (Generally Available)
- VoiceTag: Contains additional metadata for synthesis

## Next Steps

1. Add the 5 VoiceInfo entries to `config.py` in the Portuguese language section
2. Test each voice to ensure proper synthesis
3. Document any regional pronunciation differences between pt-BR and pt-PT
4. Consider setting a default voice (suggestion: pt-BR-AntonioNeural for consistency with other languages using male voices as default)
