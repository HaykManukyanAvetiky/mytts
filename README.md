# MyTTS - Text to Speech Application

A simple, free text-to-speech web application built with FastAPI and Alpine.js, powered by Microsoft Edge TTS.

## Overview

MyTTS allows content creators to quickly convert text scripts into natural-sounding speech audio files. Perfect for YouTubers, podcasters, and video editors who need high-quality voiceovers without the cost of commercial TTS services.

## Features

- **Simple Interface**: Clean, single-page application with no navigation required
- **High-Quality TTS**: Powered by Microsoft Edge TTS with natural-sounding voices
- **Multiple Voices**: Choose from various English voices with different accents and styles
- **Voice Preview**: Listen to voice samples before generating full audio
- **Speed Control**: Adjust speaking speed (0.75x, 1.0x, 1.15x, 1.25x, 1.5x)
- **Pitch Control**: Fine-tune voice pitch (-20% to +20%)
- **Fast Generation**: Convert text to speech in seconds
- **In-Browser Playback**: Preview audio before downloading
- **Easy Download**: Download generated audio as MP3 files
- **Character Counter**: Real-time feedback when approaching the 3000 character limit
- **Settings Persistence**: Speed, pitch, and voice selections are saved in your browser
- **Error Handling**: Clear, helpful error messages for common issues
- **Automatic Cleanup**: Temporary files are automatically deleted after 5 minutes

## Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **Frontend**: Alpine.js + HTML5/CSS3
- **TTS Engine**: Edge TTS (edge-tts library)
- **Template Engine**: Jinja2
- **Package Manager**: uv

## Requirements

- Python 3.10 or higher
- uv package manager

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd mytts
```

### 2. Create Virtual Environment

```bash
uv venv
```

### 3. Activate Virtual Environment

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
uv pip install -e .
```

### 5. Run the Server

```bash
uvicorn backend.main:app --reload
```

The application will be available at `http://localhost:8000`

## Usage

1. Open your browser and navigate to `http://localhost:8000`
2. Select a voice from the dropdown (click "Preview" to hear a sample)
3. Adjust speed (0.75x - 1.5x) and pitch (-20% to +20%) as desired
4. Enter your text in the textarea (1-3000 characters)
5. Click the "Generate Speech" button
6. Wait for the audio to generate
7. Preview the audio using the built-in player
8. Download the MP3 file if needed

Your voice, speed, and pitch settings are automatically saved for next time.

## Project Structure

```
mytts/
├── backend/
│   ├── api/
│   │   └── routes/
│   │       └── tts.py          # API endpoints
│   ├── core/
│   │   ├── audio/
│   │   │   └── storage.py      # Audio file management
│   │   └── tts/
│   │       ├── protocols.py    # TTS provider protocol
│   │       └── service.py      # Edge TTS implementation
│   ├── exceptions/
│   │   └── tts_exceptions.py   # Custom exceptions
│   ├── models/
│   │   ├── requests.py         # Request models
│   │   └── responses.py        # Response models
│   ├── templates/
│   │   └── index.html          # Main application page
│   ├── config.py               # Application configuration
│   └── main.py                 # FastAPI application entry point
├── static/
│   ├── css/
│   │   └── styles.css          # Application styles
│   └── js/
│       └── app.js              # Alpine.js application logic
├── pyproject.toml              # Project dependencies
└── README.md                   # This file
```

## Configuration

The application can be configured using environment variables. Create a `.env` file in the root directory:

```env
APP_NAME=MyTTS
DEBUG=False
DEFAULT_VOICE=en-US-GuyNeural
MAX_TEXT_LENGTH=3000
TEMP_DIR=/tmp/mytts_audio
CLEANUP_DELAY_SECONDS=300
```

## API Endpoints

### POST /api/tts/generate

Generate TTS audio from text.

**Request Body:**
```json
{
  "text": "Your text here",
  "voice": "en-US-GuyNeural",
  "rate": "+0%",
  "pitch": "+0Hz"
}
```

- `voice`: Voice ID (optional, defaults to en-US-GuyNeural)
- `rate`: Speed adjustment in format `+/-{number}%` (e.g., `+15%`, `-25%`)
- `pitch`: Pitch adjustment in format `+/-{number}Hz` (e.g., `+10Hz`, `-20Hz`)

**Response:**
```json
{
  "audio_url": "/api/tts/audio/mytts-2025-11-25-001516.mp3",
  "filename": "mytts-2025-11-25-001516.mp3",
  "character_count": 15,
  "generated_at": "2025-11-25T00:15:16.764125"
}
```

### GET /api/tts/audio/{filename}

Download or stream generated audio file.

**Response**: MP3 audio file

## Development

### Running Tests

```bash
pytest
```

### Code Style

The project follows:
- Modern Python 3.10+ type hints
- Async-first design patterns
- Protocol-based architecture for testability
- Comprehensive docstrings

## Limitations

- Maximum text length: 3000 characters
- Generated files are automatically deleted after 5 minutes
- English voices only
- No user accounts or saved history

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Support

For issues or questions, please open an issue on GitHub.
