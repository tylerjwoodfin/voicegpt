# VoiceGPT
This is a simple Python voice assistant powered by ChatGPT.

## dependencies

- [cabinet](https://pypi.org/project/cabinet/) (or just hardcode API key in `OPENAPI_KEY.md`)
- see `requirements.md`

## setup and installation

- clone this repo

- `pip install -r https://github.com/tylerjwoodfin/voicegpt/blob/main/requirements.md`

- if using `cabinet`, store the API key you generated from https://platform.openai.com/account/api-keys
  in `keys -> openai`:
  - `cabinet -p keys openai <your key here>`
- otherwise, replace the text in `OPENAPI_KEY.md` with the key.

### pre-launch personality configuration
- Modify `PERSONALITY.md`. Each statement should be kept on one line.

## warnings
- `gtts` is used, which interfaces with Google to convert speech to text.

## usage

- `../path/to/main.py 2>/dev/null`
  - (without `2>/dev/null`, you will likely see many unnecessary error messages due to ALSA being overly verbose)

