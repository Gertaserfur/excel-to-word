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

## Auth

Credentials are resolved in this order:

1. **Environment variables `APP_USERNAME` and `APP_PASSWORD`** — used
   when both are set. This is the path for Hugging Face Spaces (add them
   as Space secrets).
2. **`config.json` next to `app.py`** — used as a fallback when the env
   vars are not set. Convenient for local runs.

`config.json` shape:

```json
{
  "username": "admin",
  "password": "change-me"
}
```

`config.json` is gitignored — do not commit real credentials.

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
3. On the Space, go to **Settings → Variables and secrets** and add two
   secrets:
   - `APP_USERNAME` — your login username
   - `APP_PASSWORD` — your login password

   The Space exposes these as environment variables, which `app.py` picks
   up automatically. No `config.json` is needed on the Space.
4. The Space will install `requirements.txt` and start `app.py`
   automatically. Sign in with the credentials from your secrets.

Set the Space to **Private** if you don't want the auth prompt to be
publicly reachable.
