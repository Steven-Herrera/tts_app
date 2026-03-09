"""Streaming audio writer with silence padding."""

from pathlib import Path
from typing import Iterable

import numpy as np
import soundfile as sf


class AudioStreamWriter:
    """Stream audio chunks to disk safely."""

    def __init__(
        self,
        output_path: Path,
        sample_rate: int,
        silence_duration_sec: float = 0.3,
    ) -> None:
        """Initialize audio stream writer.

        Args:
            output_path: Destination WAV path.
            sample_rate: Audio sample rate.
            silence_duration_sec: Silence padding between chunks.
        """
        self._output_path = output_path
        self._sample_rate = sample_rate
        self._silence_samples = int(sample_rate * silence_duration_sec)

    def write_stream(self, audio_chunks: Iterable[np.ndarray]) -> None:
        """Write audio chunks incrementally to file.

        Args:
            audio_chunks: Iterable of numpy audio arrays.
        """
        silence = np.zeros(self._silence_samples, dtype=np.float32)

        with sf.SoundFile(
            self._output_path,
            mode="w",
            samplerate=self._sample_rate,
            channels=1,
        ) as file:
            first = True
            for chunk in audio_chunks:
                if chunk.size == 0:
                    continue

                if not first:
                    file.write(silence)

                file.write(chunk)
                first = False
