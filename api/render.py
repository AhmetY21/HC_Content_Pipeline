from __future__ import annotations

import base64
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from app.content import CATEGORIES, TONES, generate_caption
from app.emailer import send_post_email
from app.rendering import RenderError, compose_post
from app.settings import settings


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_CONTENT_LENGTH = 500
MAX_UPLOAD_BYTES = 4_500_000
ISTANBUL_TZ = ZoneInfo("Europe/Istanbul")
ROOT = Path(__file__).resolve().parents[1]

app = FastAPI(title="H&C Otomotiv Content Pipeline")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)


def _error(message: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse({"ok": False, "error": message}, status_code=status_code)


async def _handle_render(
    photo: UploadFile,
    category: str,
    tone: str,
    frame_mode: str,
    content: str,
    email: str,
    variant: int,
) -> JSONResponse:
    category = category.strip()
    tone = tone.strip()
    frame_mode = frame_mode.strip()
    content = content.strip()
    email = email.strip()

    if category not in CATEGORIES:
        return _error("Lütfen geçerli bir kategori seçin.")
    if tone not in TONES:
        return _error("Lütfen geçerli bir ton seçin.")
    if frame_mode not in {"light", "dark"}:
        return _error("Lütfen açık veya koyu çerçeve seçin.")
    if not content:
        return _error("Lütfen bir konu yazın.")
    if len(content) > MAX_CONTENT_LENGTH:
        return _error("Konu en fazla 500 karakter olabilir.")
    if not EMAIL_RE.match(email):
        return _error("Lütfen geçerli bir e-posta adresi girin.")

    photo_bytes = await photo.read()
    if not photo_bytes:
        return _error("Lütfen bir fotoğraf yükleyin.")
    if len(photo_bytes) > MAX_UPLOAD_BYTES:
        return _error("Fotoğraf çok büyük. Lütfen tekrar seçin veya normal modda çekin.")

    try:
        caption, hashtags = generate_caption(category, tone, content, variant)
        png_bytes = compose_post(photo_bytes, category, frame_mode)
        email_sent = send_post_email(
            recipient=email,
            category=category,
            caption=caption,
            hashtags=hashtags,
            png_bytes=png_bytes,
            today=datetime.now(ISTANBUL_TZ).date(),
        )
    except RenderError as exc:
        return _error(str(exc))
    except RuntimeError as exc:
        return _error(str(exc), status_code=500)
    except Exception:
        return _error("Görsel hazırlanırken beklenmeyen bir hata oluştu.", status_code=500)

    encoded = base64.b64encode(png_bytes).decode("ascii")
    return JSONResponse(
        {
            "ok": True,
            "preview_url": f"data:image/png;base64,{encoded}",
            "caption": caption,
            "hashtags": hashtags,
            "email_sent": email_sent,
        }
    )


@app.get("/api/health")
def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(ROOT / "index.html")


@app.post("/")
async def render_root(
    photo: UploadFile = File(...),
    category: str = Form(...),
    tone: str = Form(...),
    frame_mode: str = Form(...),
    content: str = Form(...),
    email: str = Form(...),
    variant: int = Form(0),
) -> JSONResponse:
    return await _handle_render(photo, category, tone, frame_mode, content, email, variant)


@app.post("/api/render")
async def render_api(
    photo: UploadFile = File(...),
    category: str = Form(...),
    tone: str = Form(...),
    frame_mode: str = Form(...),
    content: str = Form(...),
    email: str = Form(...),
    variant: int = Form(0),
) -> JSONResponse:
    return await _handle_render(photo, category, tone, frame_mode, content, email, variant)
