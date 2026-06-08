import json
import os
import re
import tempfile
from datetime import date, datetime, time, timedelta
from pathlib import Path

import gradio as gr
import pandas as pd
from docxtpl import DocxTemplate

APP_DIR = Path(__file__).parent.resolve()
TEMPLATE_PATH = APP_DIR / "template.docx"
CONFIG_PATH = APP_DIR / "config.json"

REQUIRED_COLUMNS = ["Şöför", "Saat", "Tarih", "Müşteri", "To", "From", "Kişi"]


def load_credentials():
    env_user = os.environ.get("APP_USERNAME")
    env_pw = os.environ.get("APP_PASSWORD")
    if env_user and env_pw:
        return env_user, env_pw

    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            cfg = json.load(f)
        username = cfg.get("username")
        password = cfg.get("password")
        if not username or not password:
            raise ValueError(
                'config.json must contain non-empty "username" and "password".'
            )
        return str(username), str(password)

    raise FileNotFoundError(
        "No credentials configured. Set APP_USERNAME and APP_PASSWORD "
        "environment variables (recommended for Hugging Face Spaces — "
        "add them as Space secrets), or create a config.json next to "
        f"app.py at {CONFIG_PATH} with "
        '{"username": "xxx", "password": "xxx"}.'
    )


def parse_tarih(value):
    """Return (display 'dd.mm.yyyy', sort-key date). Falls back to raw string."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "", date.min
    if isinstance(value, datetime):
        d = value.date()
        return d.strftime("%d.%m.%Y"), d
    if isinstance(value, date):
        return value.strftime("%d.%m.%Y"), value
    s = str(value).strip()
    if not s:
        return "", date.min
    for fmt in ("%d.%m.%Y", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            d = datetime.strptime(s, fmt).date()
            return d.strftime("%d.%m.%Y"), d
        except ValueError:
            continue
    return s, date.min


def parse_saat(value):
    """Return (display 'HH:MM', sort-key time)."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "", time.min
    if isinstance(value, time):
        return value.strftime("%H:%M"), value.replace(second=0, microsecond=0)
    if isinstance(value, datetime):
        t = value.time().replace(second=0, microsecond=0)
        return t.strftime("%H:%M"), t
    if isinstance(value, timedelta):
        total = int(value.total_seconds())
        h = (total // 3600) % 24
        m = (total % 3600) // 60
        t = time(h, m)
        return t.strftime("%H:%M"), t
    s = str(value).strip()
    if not s:
        return "", time.min
    try:
        f = float(s)
        total = int(round(f * 24 * 3600))
        h = (total // 3600) % 24
        m = (total % 3600) // 60
        t = time(h, m)
        return t.strftime("%H:%M"), t
    except ValueError:
        pass
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            t = datetime.strptime(s, fmt).time().replace(second=0, microsecond=0)
            return t.strftime("%H:%M"), t
        except ValueError:
            continue
    return s, time.min


def count_people(kisi) -> int:
    if kisi is None or (isinstance(kisi, float) and pd.isna(kisi)):
        return 0
    parts = [p.strip() for p in str(kisi).split(" - ")]
    parts = [p for p in parts if p]
    return len(parts)


def format_people(n: int) -> str:
    return "1 person" if n == 1 else f"{n} people"


_SAFE_NAME_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]+')


def safe_filename(name: str) -> str:
    name = (name or "document").strip()
    name = name.replace(" ", "_")
    name = _SAFE_NAME_RE.sub("", name)
    name = name.strip(". ")
    return name or "document"


def _str(value) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def render_doc(rows: list[dict], out_path: Path) -> None:
    tpl = DocxTemplate(str(TEMPLATE_PATH))
    tpl.render({"rows": rows})
    tpl.save(str(out_path))


def convert(excel_file):
    if excel_file is None:
        raise gr.Error("Please upload an .xlsx file.")
    if not TEMPLATE_PATH.exists():
        raise gr.Error(
            f"template.docx not found next to app.py (expected at {TEMPLATE_PATH}). "
            "Run create_template.py once to generate it."
        )

    src = excel_file if isinstance(excel_file, str) else excel_file.name
    try:
        df = pd.read_excel(src, engine="openpyxl")
    except Exception as e:
        raise gr.Error(f"Could not read Excel file: {e}")

    if df.empty:
        raise gr.Error("The Excel file is empty.")

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise gr.Error(
            "Missing required column(s): "
            + ", ".join(missing)
            + f". Expected columns: {', '.join(REQUIRED_COLUMNS)}."
        )

    df["_tarih_parsed"] = pd.to_datetime(
        df["Tarih"], format="%d.%m.%Y", errors="coerce"
    )
    df_sorted = df.sort_values(by=["_tarih_parsed", "Saat"])

    rows = []
    for _, row in df_sorted.iterrows():
        driver_raw = row["Şöför"]
        if pd.isna(driver_raw) or not str(driver_raw).strip():
            raise gr.Error("'Şöför' column contains empty values.")

        tarih_display, _ = parse_tarih(row["Tarih"])
        saat_display, _ = parse_saat(row["Saat"])
        kisi_raw = _str(row["Kişi"])
        people = format_people(count_people(row["Kişi"]))

        rows.append(
            {
                "Tarih": tarih_display,
                "Saat": saat_display,
                "Şöför": str(driver_raw).strip(),
                "Müşteri": _str(row["Müşteri"]),
                "To": _str(row["To"]),
                "From": _str(row["From"]),
                "NumberOfPeople": people,
                "Kişi": kisi_raw,
            }
        )

    out_dir = Path(tempfile.mkdtemp(prefix="xlsx2docx_"))
    output_filename = safe_filename(Path(src).stem) + ".docx"
    out_path = out_dir / output_filename

    try:
        render_doc(rows, out_path)
    except Exception as e:
        raise gr.Error(f"Failed to render document: {e}")

    return str(out_path)


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
                "Upload an `.xlsx` file with columns **Şöför, Saat, Tarih, "
                "Müşteri, To, From, Kişi**. All drivers and their transfers "
                "are combined into a single Word document, named after your file."
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
