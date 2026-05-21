---
title: Excel To Word
emoji: 📄
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.29.0
app_file: app.py
pinned: false
---

# Excel → Word (Gradio)

A small Gradio app that takes an `.xlsx` file and produces filled Word
documents from a `template.docx`. One row → one document. Multiple rows →
a zip.

## Files

- `app.py` — the Gradio app
- `requirements.txt` — Python dependencies
- `config.json` — username/password for Gradio basic auth
- `template.docx` — **you must provide this** (see below)

## Excel format

Columns (Turkish headers, exact match):

| Personel     | Servis Saati | Center |
|--------------|--------------|--------|
| Utku Yaldız  | 11:30:00     | İga    |
| Serdar Ortaç | 12:30:00     | Saw    |

Mapping to Word placeholders:

- `Personel` → `{{Personnel}}`
- `Servis Saati` → `{{Time}}` (formatted as `HH:MM`)
- `Center` → `{{Center}}`

## Template

Create `template.docx` next to `app.py`. Inside the document, use these
placeholders exactly:

```
Personel: {{Personnel}}
Servis Saati: {{Time}}
Center: {{Center}}
```

`docxtpl` uses Jinja2-style `{{ }}` syntax — type the braces in Word as
plain text (not as Word fields).

## Auth (config.json)

Credentials are read from `config.json` in the same directory as
`app.py`:

```json
{
  "username": "admin",
  "password": "change-me"
}
```

Change these before deploying. Do **not** commit real credentials.

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open <http://localhost:7860> and sign in with the values from
`config.json`.

Environment variables (optional):

- `GRADIO_SERVER_NAME` — bind address (default `0.0.0.0`)
- `GRADIO_SERVER_PORT` — port (default `7860`)

## Output naming

Each row produces `<Personel>.docx`, spaces replaced with underscores
(e.g. `Utku_Yaldız.docx`). Multiple rows are bundled into
`documents.zip`.

## Errors

The UI surfaces clear messages for:

- empty file uploads
- missing required columns
- empty `Personel` values
- unreadable `.xlsx` files
- missing `template.docx`

## Deploy to Hugging Face Spaces

1. Create a new Space, SDK = **Gradio**.
2. Push these files to the Space repo:
   - `app.py`
   - `requirements.txt`
   - `template.docx`
   - `README.md`
3. **Do not** commit your real `config.json`. Instead, on the Space:
   - Go to **Settings → Variables and secrets**.
   - Add a secret `CONFIG_JSON` with the JSON content, or upload a
     private `config.json` via the Files tab (private Space recommended).
4. If you use a secret, add a tiny bootstrap at the top of `app.py`
   (before `load_credentials()`) to write the secret to disk:

   ```python
   import os, pathlib
   if not (pathlib.Path(__file__).parent / "config.json").exists() and os.environ.get("CONFIG_JSON"):
       (pathlib.Path(__file__).parent / "config.json").write_text(
           os.environ["CONFIG_JSON"], encoding="utf-8"
       )
   ```

5. The Space will install `requirements.txt` and start `app.py`
   automatically. Sign in with the credentials from your config.

Set the Space to **Private** if you don't want the auth prompt to be
publicly reachable.
