"""Custom exceptions for MyTTS application.

This module defines the exception hierarchy for domain-specific errors
in the text-to-speech application.
"""


class MyTTSException(Exception):
    """Base exception for MyTTS application.

    All custom exceptions in the MyTTS application should inherit from this
    base class to allow for consistent exception handling and filtering.
    """
    pass


class TTSGenerationError(MyTTSException):
    """Raised when TTS generation fails.

    This exception indicates that the text-to-speech generation process
    encountered an error, such as issues with the TTS engine, invalid voice
    parameters, or other generation-specific failures.
    """
    pass
