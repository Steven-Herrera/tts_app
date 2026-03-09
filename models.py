"""Domain models and validation schemas."""

from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class TTSConfig(BaseModel):
    """Configuration for TTS model."""

    model_name: str = Field(..., description="Coqui TTS model name")
    use_gpu: bool = Field(default=True)

    @field_validator("model_name")
    @classmethod
    def validate_model_name(cls, value: str) -> str:
        """Validate model name is not empty."""
        if not value.strip():
            raise ValueError("Model name cannot be empty.")
        return value


class AudioConfig(BaseModel):
    """Audio output configuration."""

    sample_rate: int = Field(default=22050, gt=0)


class AppConfig(BaseModel):
    """Application configuration."""

    tts: TTSConfig
    audio: AudioConfig


class SynthesisRequest(BaseModel):
    """Represents a TTS synthesis request."""

    input_path: Path
    output_path: Path

    @field_validator("input_path")
    @classmethod
    def validate_input_exists(cls, value: Path) -> Path:
        """Ensure input file exists."""
        if not value.exists():
            raise FileNotFoundError(f"Input file not found: {value}")
        if value.suffix.lower() != ".txt":
            raise ValueError("Input file must be a .txt file.")
        return value

    @field_validator("output_path")
    @classmethod
    def validate_output_extension(cls, value: Path) -> Path:
        """Ensure output file is .wav."""
        if value.suffix.lower() != ".wav":
            raise ValueError("Output file must be a .wav file.")
        return value
