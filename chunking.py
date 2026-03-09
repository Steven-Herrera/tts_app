"""Text chunking utilities."""

import re
import textwrap
from typing import Generator


class TextChunker:
    """Production-grade text chunker for long-form synthesis."""

    def __init__(self, max_chars: int = 500) -> None:
        """Initialize chunker.

        Args:
            max_chars: Maximum characters per chunk.
        """
        self._max_chars = max_chars

    def chunk(self, text: str) -> Generator[str, None, None]:
        """Yield safe text chunks.

        Args:
            text: Full input text.

        Yields:
            Safe text chunks under max_chars.
        """
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())

        current_chunk: str = ""

        for sentence in sentences:
            if not sentence.strip():
                continue

            # Handle extremely long single sentences
            if len(sentence) > self._max_chars:
                yield from self._split_long_sentence(sentence)
                continue

            if len(current_chunk) + len(sentence) + 1 <= self._max_chars:
                current_chunk = (
                    f"{current_chunk} {sentence}".strip() if current_chunk else sentence
                )
            else:
                yield current_chunk
                current_chunk = sentence

        if current_chunk:
            yield current_chunk

    def _split_long_sentence(self, sentence: str) -> Generator[str, None, None]:
        """Split extremely long sentence safely."""
        wrapped = textwrap.wrap(
            sentence,
            width=self._max_chars,
            break_long_words=False,
            replace_whitespace=False,
        )
        for part in wrapped:
            yield part.strip()
