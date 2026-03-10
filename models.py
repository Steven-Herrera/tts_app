"""Domain models and validation schemas."""

from pathlib import Path
from typing import Dict, Literal, Optional

from pydantic import BaseModel, Field, field_validator

VoiceType = Literal["speaker", "clone"]


class VoiceProfile(BaseModel):
    """Represents a runtime voice configuration."""

    type: VoiceType
    speaker_id: Optional[str] = None
    reference_audio_path: Optional[Path] = None
    language: Optional[str] = "en"

    @field_validator("reference_audio_path")
    @classmethod
    def validate_reference_path(cls, value: Optional[Path]) -> Optional[Path]:
        if value and not value.exists():
            raise FileNotFoundError(f"Reference audio not found: {value}")
        return value

    @field_validator("speaker_id")
    @classmethod
    def validate_speaker_id(cls, value: Optional[str], info):
        voice_type = info.data.get("type")
        if voice_type == "speaker" and not value:
            raise ValueError("speaker_id must be provided for speaker type.")
        return value


class VoiceRegistry(BaseModel):
    """Collection of reusable voice presets."""

    presets: Dict[str, VoiceProfile]


class DefaultVoiceConfig(BaseModel):
    """Defines default voice preset."""

    preset: Optional[str] = None


class TTSConfig(BaseModel):
    """Configuration for TTS model."""

    model_name: str
    use_gpu: bool = True
    default_voice: Optional[DefaultVoiceConfig] = None


class AudioConfig(BaseModel):
    """Audio output configuration."""

    sample_rate: int = Field(default=22050, gt=0)


class AppConfig(BaseModel):
    """Application configuration."""

    tts: TTSConfig
    audio: AudioConfig
    voices: Optional[VoiceRegistry] = None


class SynthesisRequest(BaseModel):
    """Represents a TTS synthesis request."""

    input_path: Path
    output_path: Path
    voice_profile: Optional[VoiceProfile] = None
