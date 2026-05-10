"""
utils/transcriber.py
Speech-to-text using faster-whisper (local, no OpenAI API needed).
"""
import os
import tempfile
from pathlib import Path

# Lazy import to avoid loading heavy model at startup
_model = None


def _get_model(model_size: str = "base"):
    """Load and cache the Whisper model."""
    global _model
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise ImportError(
            "faster-whisper is not installed. Run: pip install faster-whisper"
        )

    if _model is None:
        # Use CPU with int8 quantisation for lightweight inference
        _model = WhisperModel(model_size, device="cpu", compute_type="int8")
    return _model


def transcribe_audio(audio_bytes: bytes, filename: str = "audio.wav", model_size: str = "base") -> dict:
    """
    Transcribe audio bytes using faster-whisper.

    Args:
        audio_bytes: Raw audio bytes.
        filename:    Original filename (used to infer extension).
        model_size:  Whisper model size — tiny | base | small | medium | large-v2

    Returns:
        dict with keys: text, language, duration_seconds
    """
    suffix = Path(filename).suffix or ".wav"

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        model = _get_model(model_size)
        segments, info = model.transcribe(tmp_path, beam_size=5)

        full_text = " ".join(seg.text.strip() for seg in segments)
        return {
            "text": full_text.strip(),
            "language": info.language,
            "duration_seconds": round(info.duration, 1),
        }
    finally:
        os.unlink(tmp_path)


def get_available_model_sizes() -> list:
    return ["tiny", "base", "small", "medium", "large-v2"]