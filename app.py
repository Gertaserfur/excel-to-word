import io
import json
import os
import re
import tempfile
import zipfile
from datetime import datetime, time, timedelta
from pathlib import Path

import gradio as gr
import pandas as pd
from docxtpl import DocxTemplate

APP_DIR = Path(__file__).parent.resolve()
TEMPLATE_PATH = APP_DIR / "template.docx"
CONFIG_PATH = APP_DIR / "config.json"

COLUMN_MAP = {
    "Personel": "Personnel",
    "Servis Saati": "Time",
    "Center": "Center",
}


def load_credentials():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"config.json not found at {CONFIG_PATH}. "
            'Create it with {"username": "xxx", "password": "xxx"}.'
        )
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        cfg = json.load(f)
    username = cfg.get("username")
    password = cfg.get("password")
    if not username or not password:
        raise ValueError('config.json must contain non-empty "username" and "password".')
    return str(username), str(password)


def format_time(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and pd.isna(value):
        return ""
    if isinstance(value, time):
        return value.strftime("%H:%M")
    if isinstance(value, datetime):
        return value.strftime("%H:%M")
    if isinstance(value, timedelta):
        total = int(value.total_seconds())
        h = (total // 3600) % 24
        m = (total % 3600) // 60
        return f"{h:02d}:{m:02d}"
    s = str(value).strip()
    if not s:
        return ""
    # Excel may give "HH:MM:SS" or "HH:MM" or a fractional day number as string
    try:
        f = float(s)
        total = int(round(f * 24 * 3600))
        h = (total // 3600) % 24
        m = (total % 3600) // 60
        return f"{h:02d}:{m:02d}"
    except ValueError:
        pass
    parts = s.split(":")
    if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
        return f"{int(parts[0]):02d}:{int(parts[1]):02d}"
    return s


_SAFE_NAME_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]+')


def safe_filename(name: str) -> str:
    name = (name or "document").strip()
    name = name.replace(" ", "_")
    name = _SAFE_NAME_RE.sub("", name)
    name = name.strip(". ")
    return name or "document"


def render_doc(row: pd.Series, out_path: Path) -> None:
    tpl = DocxTemplate(str(TEMPLATE_PATH))
    context = {
        "Personnel": "" if pd.isna(row["Personel"]) else str(row["Personel"]).strip(),
        "Time": format_time(row["Servis Saati"]),
        "Center": "" if pd.isna(row["Center"]) else str(row["Center"]).strip(),
    }
    tpl.render(context)
    tpl.save(str(out_path))


def convert(excel_file):
    if excel_file is None:
        raise gr.Error("Please upload an .xlsx file.")
    if not TEMPLATE_PATH.exists():
        raise gr.Error(
            f"template.docx not found next to app.py (expected at {TEMPLATE_PATH})."
        )

    src = excel_file if isinstance(excel_file, str) else excel_file.name
    try:
        df = pd.read_excel(src, engine="openpyxl")
    except Exception as e:
        raise gr.Error(f"Could not read Excel file: {e}")

    if df.empty:
        raise gr.Error("The Excel file is empty.")

    missing = [c for c in COLUMN_MAP if c not in df.columns]
    if missing:
        raise gr.Error(
            "Missing required column(s): "
            + ", ".join(missing)
            + f". Expected columns: {', '.join(COLUMN_MAP.keys())}."
        )

    out_dir = Path(tempfile.mkdtemp(prefix="xlsx2docx_"))
    generated: list[Path] = []
    used_names: dict[str, int] = {}

    for idx, row in df.iterrows():
        personel_raw = row["Personel"]
        if pd.isna(personel_raw) or not str(personel_raw).strip():
            raise gr.Error(f"Row {idx + 2}: 'Personel' is empty.")
        base = safe_filename(str(personel_raw))
        count = used_names.get(base, 0) + 1
        used_names[base] = count
        filename = f"{base}.docx" if count == 1 else f"{base}_{count}.docx"
        out_path = out_dir / filename
        try:
            render_doc(row, out_path)
        except Exception as e:
            raise gr.Error(f"Row {idx + 2}: failed to render document — {e}")
        generated.append(out_path)

    if len(generated) == 1:
        return str(generated[0])

    zip_path = out_dir / "documents.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in generated:
            zf.write(p, arcname=p.name)
    return str(zip_path)


def attempt_login(username: str, password: str, logged_in: bool):
    try:
        expected_user, expected_pw = load_credentials()
    except Exception as e:
        return (
            logged_in,
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(value=f"Login unavailable: {e}", visible=True),
        )

    if (username or "") == expected_user and (password or "") == expected_pw:
        return (
            True,
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(value="", visible=False),
        )

    return (
        False,
        gr.update(visible=True),
        gr.update(visible=False),
        gr.update(value="Invalid username or password.", visible=True),
    )


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Excel → Word") as demo:
        logged_in = gr.State(False)

        with gr.Column(visible=True) as login_screen:
            gr.Markdown("# Sign in\nEnter your credentials to continue.")
            username_in = gr.Textbox(label="Username", autofocus=True)
            password_in = gr.Textbox(label="Password", type="password")
            login_btn = gr.Button("Login", variant="primary")
            login_error = gr.Markdown(visible=False)

        with gr.Column(visible=False) as app_screen:
            gr.Markdown(
                "# Excel → Word\n"
                "Upload an `.xlsx` file with columns **Personel**, **Servis Saati**, **Center**. "
                "Each row produces one Word document from `template.docx`. "
                "Multiple rows are returned as a zip."
            )
            with gr.Row():
                inp = gr.File(label="Excel file (.xlsx)", file_types=[".xlsx"])
            btn = gr.Button("Convert", variant="primary")
            out = gr.File(label="Download")
            btn.click(fn=convert, inputs=inp, outputs=out)

        login_btn.click(
            fn=attempt_login,
            inputs=[username_in, password_in, logged_in],
            outputs=[logged_in, login_screen, app_screen, login_error],
        )
        password_in.submit(
            fn=attempt_login,
            inputs=[username_in, password_in, logged_in],
            outputs=[logged_in, login_screen, app_screen, login_error],
        )
    return demo


if __name__ == "__main__":
    ui = build_ui()
    ui.launch(
        ssr_mode=False,
        server_name=os.environ.get("GRADIO_SERVER_NAME", "0.0.0.0"),
        server_port=int(os.environ.get("GRADIO_SERVER_PORT", "7860")),
    )
