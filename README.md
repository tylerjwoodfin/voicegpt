# VoiceGPT
This is a simple Python voice assistant powered by ChatGPT, designed for Debian-based Linux (e.g. Ubuntu).

## dependencies

- [cabinet](https://pypi.org/project/cabinet/) (or just hardcode API key in `OPENAPI_KEY.md`)
- see `requirements.md`

## setup and installation

- clone this repo

- run:
```
sudo apt-get install sox libsox-fmt-all
sudo apt-get install espeak libespeak1 libespeak-dev
sudo apt-get install portaudio19-dev
pip install -r https://raw.githubusercontent.com/tylerjwoodfin/voicegpt/main/requirements.md
```

- if using `cabinet`, store the API key you generated from https://platform.openai.com/account/api-keys
  in `keys -> openai`:
  - `cabinet -p keys openai <your key here>`
- otherwise, replace the text in `OPENAPI_KEY.md` with the key.

### pre-launch personality configuration
- Modify `PERSONALITY.md`. Each statement should be kept on one line.

## adding custom commands
- by default, VoiceGPT will send all user input to ChatGPT. However, the `parse()` function can
  run any other code as needed based on user input.

- To avoid incompatibilities and runtime errors, `parse()` will not run unless 
  `voicegpt` -> `parse_enabled` is set to True in Cabinet...
  or simply remove this check; you're editing the code as it is, anyway.
- `cabinet -p voicegpt parse_enabled true`
- modify `parse()` as needed

## warnings
- `gtts` is used, which interfaces with Google to convert speech to text.

## usage

- `../path/to/main.py 2>/dev/null`
  - (without `2>/dev/null`, you will likely see many unnecessary error messages due to ALSA being overly verbose)

