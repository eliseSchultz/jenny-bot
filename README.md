# jenny-bot
LLM TTS Discord Bot using Coqui.ai. "Jenny" is named after the default model `tts_models/en/jenny/jenny`.

Tested on Python `3.10.12`

```
pip install -e .
```

Make a `secret.py` containing:

```
TOKEN = "<Discord Token string>"
```
To run:

```
python3 jenny.py
```

## Planned Features:
 - CLI options to specify which model to use
 - Extensive logging overhaul
 - Implement speech recipes for client side users