"""TTS engine abstraction and implementation."""

from abc import ABC, abstractmethod
from typing import Generator, Optional

import numpy as np
import torch
from TTS.api import TTS

from models import TTSConfig, VoiceProfile


class TextToSpeechEngine(ABC):
    """Abstract TTS engine."""

    @abstractmethod
    def synthesize_stream(
        self,
        text_chunks: Generator[str, None, None],
        voice_profile: Optional[VoiceProfile],
    ) -> Generator[np.ndarray, None, None]:
        pass


class CoquiTTSEngine(TextToSpeechEngine):
    """Coqui TTS engine implementation."""

    def __init__(self, config: TTSConfig) -> None:
        self._device = "cuda" if config.use_gpu and torch.cuda.is_available() else "cpu"
        self._tts = TTS(model_name=config.model_name).to(self._device)

    def synthesize_stream(
        self,
        text_chunks: Generator[str, None, None],
        voice_profile: Optional[VoiceProfile],
    ) -> Generator[np.ndarray, None, None]:

        for i, chunk in enumerate(text_chunks, 1):
            print(f"Synthesizing chunk {i}...")

            inference_kwargs = {}

            if voice_profile:
                if voice_profile.type == "speaker":
                    inference_kwargs["speaker"] = voice_profile.speaker_id

                elif voice_profile.type == "clone":
                    inference_kwargs["speaker_wav"] = str(
                        voice_profile.reference_audio_path
                    )
                    if voice_profile.language:
                        inference_kwargs["language"] = voice_profile.language

            wav = self._tts.tts(chunk, **inference_kwargs)

            yield np.asarray(wav, dtype=np.float32)
