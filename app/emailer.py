from __future__ import annotations

import smtplib
from datetime import date
from email.message import EmailMessage

from .content import CATEGORIES, format_turkish_date
from .settings import settings


def build_email_body(caption: str, hashtags: str) -> str:
    return f"""✅ Instagram postunuz hazır.

Görsel ek olarak bu e-postaya iliştirildi.
Açıklama metni ve hashtag'ler aşağıda — kopyala/yapıştır ile kullanabilirsiniz.

──────────  AÇIKLAMA  ──────────

{caption}

──────────  HASHTAG  ──────────

{hashtags}

──────────  KULLANIM  ──────────

1. Eki indir ve telefonun galerisine kaydet
2. Instagram → Yeni gönderi → fotoğrafı seç
3. Yukarıdaki açıklama ve hashtag'i yapıştır → paylaş

— H&C Otomotiv Pipeline v0
"""


def send_post_email(
    *,
    recipient: str,
    category: str,
    caption: str,
    hashtags: str,
    png_bytes: bytes,
    today: date | None = None,
) -> bool:
    if not settings.send_email:
        return False
    if not settings.smtp_user or not settings.smtp_password:
        raise RuntimeError("Gmail SMTP bilgileri eksik. GMAIL_USER ve GMAIL_APP_PASSWORD ayarlanmalı.")

    today = today or date.today()
    category_label = CATEGORIES[category].label
    filename = f"post-{today.isoformat()}-{category}.png"

    message = EmailMessage()
    message["Subject"] = f"[H&C Posts] {category_label} — {format_turkish_date(today)}"
    message["From"] = settings.smtp_from or settings.smtp_user
    message["To"] = recipient
    message.set_content(build_email_body(caption, hashtags), charset="utf-8")
    message.add_attachment(
        png_bytes,
        maintype="image",
        subtype="png",
        filename=filename,
    )

    with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, timeout=20) as smtp:
        smtp.login(settings.smtp_user, settings.smtp_password)
        smtp.send_message(message)

    return True

