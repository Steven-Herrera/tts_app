"""Voice preset resolution logic."""

from typing import Optional

from models import AppConfig, VoiceProfile


class VoiceResolver:
    """Resolves voice profiles from config presets."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config

    def resolve(self, override: Optional[VoiceProfile]) -> Optional[VoiceProfile]:
        """Resolve final voice profile.

        Priority:
        1. Request override
        2. Default preset from config
        3. None
        """
        if override:
            return override

        if (
            self._config.tts.default_voice
            and self._config.tts.default_voice.preset
            and self._config.voices
        ):
            preset_name = self._config.tts.default_voice.preset
            return self._config.voices.presets.get(preset_name)

        return None
