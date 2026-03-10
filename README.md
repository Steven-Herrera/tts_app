# TTS App

Ingests a text file and returns an audio file.

## Requirements
* ffmpg
* Microsoft Visual Studio
* eSpeak

### .wav
You can convert .m4a files to .wav using ffmpeg
```powershell
ffmpeg -i voices\<name>\reference.m4a -ac 1 -ar 22050 voices\<name>\reference.wav
```

XTTS performs best with:

Mono

16kHz or 22.05kHz

Clean speech

6–15 seconds

No silence padding

No music

If you want optimal:

ffmpeg -i reference.m4a -ac 1 -ar 16000 reference.wav

### Voices
p260

