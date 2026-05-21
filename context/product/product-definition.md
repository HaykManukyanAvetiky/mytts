# Product Definition: MyTTS

- **Version:** 1.0
- **Status:** Proposed

---

## 1. The Big Picture (The "Why")

### 1.1. Project Vision & Purpose

To provide content creators with a fast, free, and simple text-to-speech tool that generates high-quality voiceovers for videos and podcasts, eliminating the need for expensive TTS services or recording their own voice.

### 1.2. Target Audience

Content creators including YouTubers, podcasters, video editors, and social media creators who need voiceovers for their content but prefer not to use their own voice or pay for professional voice services.

### 1.3. User Personas

- **Persona 1: "Alex the YouTube Explainer"**
  - **Role:** Educational content creator on YouTube making 3-5 videos per week.
  - **Goal:** Needs consistent, natural-sounding voiceovers for explainer videos without spending money on TTS services.
  - **Frustration:** Commercial TTS services are expensive for daily use, and recording own voice is time-consuming and inconsistent.

- **Persona 2: "Jordan the Podcast Producer"**
  - **Role:** Freelance podcast editor who adds narration segments to client podcasts.
  - **Goal:** Quickly generate voiceover segments for intros, outros, and transitions.
  - **Frustration:** Needs a reliable tool that works every day without usage limits or quality degradation.

### 1.4. Success Metrics

- Voice quality is natural-sounding enough for professional content use.
- The app reliably generates at least 2 hours of audio per day without failures or service interruptions.
- Users can create their first voiceover within 1 minute of opening the app.
- Generated audio is ready to use without significant post-processing.

---

## 2. The Product Experience (The "What")

### 2.1. Core Features

- Simple text input field for entering script or content
- Voice/accent selection dropdown (multiple English voices)
- Speech rate control (0.75x, 1.0x, 1.15x, 1.25x, 1.5x) for adjusting speaking speed
- Pitch control (-20%, -10%, 0%, +10%, +20%) for voice tone adjustment
- Instant in-browser audio playback
- Download generated audio as MP3 file
- Single-page interface requiring no navigation

### 2.2. User Journey

A content creator visits the MyTTS web app, pastes their video script into the text field, selects a preferred voice from the dropdown menu, clicks the "Generate" button, listens to the preview in the browser, and downloads the audio file to use in their video editing software.

---

## 3. Project Boundaries

### 3.1. What's In-Scope for this Version

- Single-page web application with minimal interface
- Text input field (plain text only)
- Voice selection dropdown with multiple English accent options
- Generate button to create TTS audio
- In-browser audio player for previewing
- Download button for MP3 file output
- Built with Python web framework (Flask or FastAPI)
- Integration with free TTS API (gTTS or Edge TTS)
- Basic error handling for API failures

### 3.2. What's Out-of-Scope (Non-Goals)

- User accounts, authentication, or login system
- Saved history of previous generations
- Batch processing of multiple texts
- Rich text editing features (spell check, formatting)
- Languages other than English
- Audio editing or post-processing features
- Mobile native application
- Text-to-speech for uploaded documents
- Cloud storage or file management
