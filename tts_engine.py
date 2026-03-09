"""TTS engine abstraction and implementation."""

from abc import ABC, abstractmethod
from typing import Generator, Optional

import numpy as np
import torch
from TTS.api import TTS

from models import TTSConfig


class TextToSpeechEngine(ABC):
    """Abstract TTS engine."""

    @abstractmethod
    def synthesize_stream(
        self, text_chunks: Generator[str, None, None]
    ) -> Generator[np.ndarray, None, None]:
        """Stream synthesized audio chunks."""
        pass


class CoquiTTSEngine(TextToSpeechEngine):
    """Coqui TTS engine implementation."""

    def __init__(self, config: TTSConfig) -> None:
        self._device = "cuda" if config.use_gpu and torch.cuda.is_available() else "cpu"
        self._tts = TTS(model_name=config.model_name).to(self._device)
        self._speaker_id = config.speaker_id

    def synthesize_stream(
        self, text_chunks: Generator[str, None, None]
    ) -> Generator[np.ndarray, None, None]:
        for i, chunk in enumerate(text_chunks, 1):
            print(f"Synthesizing chunk {i}...")

            if self._speaker_id:
                wav = self._tts.tts(chunk, speaker=self._speaker_id)
            else:
                wav = self._tts.tts(chunk)

            yield np.asarray(wav, dtype=np.float32)
