# jenny-bot
LLM TTS Discord Bot using Coqui.ai. "Jenny" is named after the default model `tts_models/en/jenny/jenny`.

Tested on Python `3.10.12`

```
pip install -r requirements.txt
```

Make a `secret.py` containing:

```
TOKEN = "<Discord Token string>"
```

## Usage


Allows specifying TTS model when launching:

```
python3 jenny.py <model-path>
```

While connected to a voice channel, use /join to have Jenny join your voice channel and begin reading the text channel. Then, use /leave for Jenny to leave and stop reading.

## Planned Features
 - Extensive logging overhaul
 - Implement speech recipes for client side users
