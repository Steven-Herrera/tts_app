"""Application services layer."""

from audio_writer import AudioStreamWriter
from chunking import TextChunker
from models import SynthesisRequest
from tts_engine import TextToSpeechEngine
from voice_registry import VoiceResolver


class TTSService:
    """Streaming audiobook synthesis service."""

    def __init__(
        self,
        engine: TextToSpeechEngine,
        chunker: TextChunker,
        writer: AudioStreamWriter,
        voice_resolver: VoiceResolver,
    ) -> None:
        self._engine = engine
        self._chunker = chunker
        self._writer = writer
        self._voice_resolver = voice_resolver

    def process(self, request: SynthesisRequest) -> None:
        text = request.input_path.read_text(encoding="utf-8")
        chunks = self._chunker.chunk(text)

        voice_profile = self._voice_resolver.resolve(request.voice_profile)

        audio_stream = self._engine.synthesize_stream(
            chunks,
            voice_profile,
        )

        self._writer.write_stream(audio_stream)
