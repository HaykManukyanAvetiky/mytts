/**
 * Alpine.js application for MyTTS text-to-speech interface
 */

function ttsApp() {
    return {
        // State properties
        text: '',
        isLoading: false,
        error: null,
        success: false,
        audioUrl: null,

        // Voice selection state
        voices: [],
        selectedVoice: null,
        loadingVoices: false,
        previewingVoice: null,
        previewAudio: null,

        // Voice control settings
        selectedRate: '1.0x',
        rateOptions: ['0.75x', '1.0x', '1.15x', '1.25x', '1.5x'],
        selectedPitch: '0%',
        pitchOptions: ['-20%', '-10%', '0%', '+10%', '+20%'],

        // Language selection state
        selectedLanguage: 'English',
        languages: [],

        /**
         * Initialize the application - load voices and restore selection
         */
        async init() {
            await this.loadVoices();
            this.restoreVoiceSelection();
            this.restoreVoiceControls();
        },

        /**
         * Load available voices from the API
         */
        async loadVoices() {
            this.loadingVoices = true;

            try {
                const response = await fetch('/api/tts/voices');
                if (response.ok) {
                    const data = await response.json();
                    this.voices = data.voices;

                    // Set default voice if none selected
                    if (!this.selectedVoice && this.voices.length > 0) {
                        this.selectedVoice = this.voices[0].id;
                    }
                }
            } catch (err) {
                console.error('Failed to load voices:', err);
            } finally {
                this.loadingVoices = false;
            }
        },

        /**
         * Restore voice selection from localStorage
         */
        restoreVoiceSelection() {
            const saved = localStorage.getItem('selectedVoice');
            if (saved && this.voices.find(v => v.id === saved)) {
                this.selectedVoice = saved;
            }
        },

        /**
         * Save voice selection to localStorage
         */
        saveVoiceSelection() {
            if (this.selectedVoice) {
                localStorage.setItem('selectedVoice', this.selectedVoice);
            }
        },

        /**
         * Handle voice dropdown change
         */
        onVoiceChange() {
            this.saveVoiceSelection();
        },

        /**
         * Save voice control settings to localStorage
         */
        saveVoiceControls() {
            localStorage.setItem('selectedRate', this.selectedRate);
            localStorage.setItem('selectedPitch', this.selectedPitch);
        },

        /**
         * Restore voice control settings from localStorage
         */
        restoreVoiceControls() {
            const savedRate = localStorage.getItem('selectedRate');
            const savedPitch = localStorage.getItem('selectedPitch');
            if (savedRate && this.rateOptions.includes(savedRate)) {
                this.selectedRate = savedRate;
            }
            if (savedPitch && this.pitchOptions.includes(savedPitch)) {
                this.selectedPitch = savedPitch;
            }
        },

        /**
         * Handle rate change
         */
        onRateChange() {
            console.log('Rate changed to:', this.selectedRate, '→', this.convertRate(this.selectedRate));
            this.saveVoiceControls();
        },

        /**
         * Handle pitch change
         */
        onPitchChange() {
            console.log('Pitch changed to:', this.selectedPitch, '→', this.convertPitch(this.selectedPitch));
            this.saveVoiceControls();
        },

        /**
         * Get formatted label for voice display
         */
        getVoiceLabel(voice) {
            return `${voice.name} (${voice.gender}, ${voice.accent})`;
        },

        /**
         * Preview a voice by playing its sample audio
         */
        async previewVoice(voiceId) {
            // Stop currently playing preview if same voice clicked
            if (this.previewingVoice === voiceId && this.previewAudio) {
                this.previewAudio.pause();
                this.previewAudio = null;
                this.previewingVoice = null;
                return;
            }

            // Stop any currently playing preview
            if (this.previewAudio) {
                this.previewAudio.pause();
                this.previewAudio = null;
            }

            // Create and play new preview
            const previewUrl = `/api/tts/preview/${voiceId}`;
            this.previewAudio = new Audio(previewUrl);
            this.previewingVoice = voiceId;

            // Handle when preview ends
            this.previewAudio.onended = () => {
                this.previewingVoice = null;
                this.previewAudio = null;
            };

            // Handle errors
            this.previewAudio.onerror = () => {
                this.showError('Failed to load voice preview. Please try again.');
                this.previewingVoice = null;
                this.previewAudio = null;
            };

            // Play the preview
            try {
                await this.previewAudio.play();
            } catch (err) {
                this.showError('Failed to play voice preview. Please try again.');
                this.previewingVoice = null;
                this.previewAudio = null;
            }
        },

        /**
         * Show error message with auto-dismiss after 5 seconds
         */
        showError(message) {
            this.error = message;
            setTimeout(() => {
                this.error = null;
            }, 5000);
        },

        /**
         * Show success message with auto-dismiss after 3 seconds
         */
        showSuccess() {
            this.success = true;
            setTimeout(() => {
                this.success = false;
            }, 3000);
        },

        /**
         * Convert rate (0.75x, 1.0x, etc.) to edge-tts format (+0%, -25%, etc.)
         */
        convertRate(rate) {
            const multiplier = parseFloat(rate);  // "1.25x" → 1.25
            const percentage = Math.round((multiplier - 1) * 100);
            return percentage >= 0 ? `+${percentage}%` : `${percentage}%`;
        },

        /**
         * Convert pitch (-20%, +10%, etc.) to edge-tts format (-20Hz, +10Hz, etc.)
         */
        convertPitch(pitch) {
            // Handle "0%" special case - needs "+" prefix
            if (pitch === '0%') {
                return '+0Hz';
            }
            return pitch.replace('%', 'Hz');
        },

        /**
         * Generate audio from text using the TTS API
         */
        async generateAudio() {
            // Client-side validation
            if (this.text.trim().length === 0) {
                this.showError('Please enter at least 1 character to generate audio.');
                return;
            }

            if (this.text.length > 3000) {
                this.showError('Text exceeds 3000 character limit. Please shorten your text to continue.');
                return;
            }

            // Clear previous audio player and errors
            this.audioUrl = null;
            this.error = null;
            this.success = false;

            // Set loading state
            this.isLoading = true;

            try {
                // Build request payload
                const payload = {
                    text: this.text,
                    voice: this.selectedVoice,
                    rate: this.convertRate(this.selectedRate),
                    pitch: this.convertPitch(this.selectedPitch)
                };
                console.log('Generating audio with:', payload);

                // Make POST request to generate endpoint
                const response = await fetch('/api/tts/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(payload),
                });

                // Check if request was successful
                if (response.ok) {
                    const data = await response.json();

                    // Set audio URL for player
                    this.audioUrl = data.audio_url;

                    // Show success indicator
                    this.showSuccess();
                } else {
                    // Handle error response
                    const errorData = await response.json();
                    this.showError(errorData.detail || errorData.message || 'Unable to generate audio at this time. Please try again in a few moments.');
                }
            } catch (err) {
                // Handle network errors
                this.showError('Connection error. Please check your internet connection and try again.');
            } finally {
                // Clear loading state
                this.isLoading = false;
            }
        }
    };
}
