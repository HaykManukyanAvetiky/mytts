# System Architecture Overview: MyTTS

---

## 1. Application & Technology Stack

- **Backend Framework:** FastAPI (Python 3.10+)
  - Async-capable for efficient TTS generation
  - Automatic API documentation
  - Fast development and excellent performance

- **Frontend:** Alpine.js + HTML5/CSS3
  - Minimal JavaScript framework for reactivity
  - No build tools required
  - Single HTML page with inline or CDN-hosted assets

- **Template Engine:** Jinja2 (built into FastAPI)
  - Serve the single-page HTML interface
  - Minimal templating needs

- **TTS Engine:** Edge TTS (edge-tts Python library)
  - Microsoft's text-to-speech API
  - Multiple high-quality English voices
  - Free and unlimited usage
  - Supports 2+ hours of daily generation

---

## 2. Data & Persistence

- **Audio File Storage:** Temporary file system (`/tmp` or OS temp directory)
  - Generated MP3 files stored temporarily
  - Automatic cleanup after serving or on app restart
  - No permanent storage required

- **Database:** None
  - Stateless application design
  - No user accounts or history tracking in Phase 1
  - No persistent data requirements

- **Session Management:** None
  - No user authentication
  - No session state required

---

## 3. Infrastructure & Deployment

- **Development Environment:** Local Python environment
  - Python 3.10 or higher
  - Virtual environment (venv or poetry)
  - Local development server (uvicorn)

- **Deployment Model:** Single container/process
  - Docker container (optional, for consistency)
  - Direct uvicorn process execution
  - Suitable for local or simple cloud deployment

- **Future Hosting Options (Post-Phase 1):**
  - Free tier: Render, Railway, or Fly.io
  - Cloud providers: AWS EC2, GCP Compute, Azure VM
  - Self-hosted: Any Linux VPS

- **Static Assets Serving:** FastAPI static file serving
  - Serve HTML, CSS, and JavaScript directly from FastAPI
  - Alpine.js loaded from CDN (jsDelivr or unpkg)

---

## 4. External Services & Dependencies

- **Primary Dependencies:**
  - `fastapi` - Web framework
  - `uvicorn` - ASGI server
  - `edge-tts` - Text-to-speech generation
  - `python-multipart` - Form handling (if needed)

- **Frontend Dependencies (CDN):**
  - Alpine.js (~15KB) - Reactivity and UI interactions
  - Simple CSS framework or custom CSS

- **No Third-Party Services:**
  - No authentication providers
  - No cloud storage (S3, etc.)
  - No monitoring or analytics in Phase 1
  - No rate limiting services

---

## 5. Security & Performance Considerations

- **Security:**
  - Input validation on text length (prevent abuse)
  - Basic error handling to avoid information leakage
  - No sensitive data storage
  - CORS configuration for API endpoints

- **Performance:**
  - Async TTS generation to avoid blocking
  - Temporary file cleanup to prevent disk space issues
  - Reasonable text length limits (e.g., 5000 characters)
  - Response compression for audio files

- **Scalability (Future):**
  - Stateless design allows horizontal scaling
  - Can add Redis for rate limiting if needed
  - Can move to object storage (S3) for large-scale deployments

---

## 6. Desktop Application (Phase 5)

- **Desktop Framework:** Tauri 2.x
  - Rust-based desktop application framework
  - Native macOS integration (menu bar, file dialogs, keyboard shortcuts)
  - Minimal bundle size (~5-10MB)
  - Uses system WebView (no bundled Chromium)

- **Frontend:** Existing Alpine.js + HTML/CSS
  - Reuse web UI code without modification
  - Served locally within Tauri app
  - No external CDN dependencies (bundle Alpine.js locally)

- **TTS Backend:** Native Rust Implementation
  - Direct Edge TTS API calls from Rust (using `edge-tts` crate or HTTP client)
  - No Python runtime bundled
  - Async Rust for non-blocking TTS generation

- **Desktop Features:**
  - Native file save dialogs for MP3 export
  - Menu bar integration with common actions
  - Keyboard shortcuts (Cmd+G for generate, Cmd+S for save)
  - macOS code signing for distribution

- **Build & Distribution:**
  - `tauri build` for macOS .app bundle
  - DMG installer for easy distribution
  - Optional: Mac App Store submission (requires Apple Developer account)

---

## 7. Testing & Quality Assurance

- **Test Framework:** pytest
  - Standard Python testing framework
  - Built-in fixtures, parameterization, and test discovery
  - Excellent FastAPI integration via `pytest-asyncio` and `httpx`

- **Test Structure:**
  - `tests/` - Root test directory
  - `tests/unit/` - Unit tests for voice validation, TTS generation logic
  - `tests/integration/` - API endpoint tests using TestClient
  - `tests/fixtures/` - Sample audio files, mock data
  - `tests/reports/` - Archived test reports and summaries

- **Test Dependencies:**
  - `pytest` - Test runner
  - `pytest-asyncio` - Async test support for FastAPI
  - `httpx` - Async HTTP client for API testing
  - `pytest-cov` (optional) - Code coverage reporting

- **Test Categories:**
  - Voice validation tests (verify voice IDs work with Edge TTS)
  - API endpoint tests (generate, voices list, health check)
  - Error handling tests (invalid input, API failures)
  - Speed/pitch parameter tests

---

## Architecture Principles

1. **Simplicity First:** Minimal dependencies, no unnecessary complexity
2. **Stateless Design:** No database or persistent storage in Phase 1
3. **Free & Open:** All technologies are free and open-source
4. **Fast Development:** Quick iteration and deployment
5. **Future-Ready:** Architecture can evolve to support accounts, history, and scaling in future phases
6. **Code Reuse:** Desktop app shares frontend code with web version
7. **Test-Driven Quality:** Comprehensive test suite ensures reliability across voice configurations and API changes
