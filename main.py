"""Application entry point."""

from audio_writer import AudioStreamWriter
from chunking import TextChunker
from config import load_config
from models import SynthesisRequest
from services import TTSService
from tts_engine import CoquiTTSEngine
from utils import parse_args


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    request = SynthesisRequest(
        input_path=args.input,
        output_path=args.output,
    )

    engine = CoquiTTSEngine(config.tts)
    chunker = TextChunker(max_chars=500)
    writer = AudioStreamWriter(
        output_path=request.output_path,
        sample_rate=config.audio.sample_rate,
        silence_duration_sec=0.3,
    )

    service = TTSService(engine, chunker, writer)
    service.process(request)


if __name__ == "__main__":
    main()
