from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "465"))
    smtp_user: str = os.getenv("GMAIL_USER", os.getenv("SMTP_USER", ""))
    smtp_password: str = os.getenv("GMAIL_APP_PASSWORD", os.getenv("SMTP_PASSWORD", ""))
    smtp_from: str = os.getenv("SMTP_FROM", os.getenv("GMAIL_USER", os.getenv("SMTP_USER", "")))
    default_recipient: str = os.getenv("DEFAULT_RECIPIENT_EMAIL", "")
    send_email: bool = os.getenv("SEND_EMAIL", "true").lower() not in {"0", "false", "no"}


settings = Settings()

