# H&C Otomotiv Content Pipeline

Python-backed Instagram post generator for H&C Otomotiv. The operator uploads one vehicle photo, chooses a v0 content category, frame mode, tone, and destination email. The API renders an Instagram-ready PNG, emails it with the generated caption and hashtags, and returns an inline browser preview.

## v0 Features

- Four production categories:
  - Günlük İş: 1080×1080
  - Kampanya / İndirim: 1080×1080
  - Müşteri Memnuniyeti: 1080×1080
  - Çekici Hizmeti: 1080×1350
- Browser-side photo downscale to JPEG at max 2048×2048 before upload.
- Light and dark H&C frame modes.
- Turkish caption and hashtag generation ported from the existing HTML tool.
- Gmail SMTP delivery with PNG attachment.
- Inline PNG preview and download fallback after submit.
- Stateless FastAPI backend, suitable for Vercel Python functions.

## Project Structure

```text
.
├── api/render.py          # FastAPI endpoint for /api/render
├── app/content.py         # Categories, templates, ideas, hashtags
├── app/emailer.py         # Gmail SMTP email body and attachment delivery
├── app/rendering.py       # Pillow image composition
├── app/settings.py        # Environment-based settings
├── assets/                # Optional logo and font assets
├── index.html             # Static operator UI
├── requirements.txt
└── vercel.json
```

## Required Environment Variables

Set these in Vercel before deploying:

```bash
GMAIL_USER=hcposts@gmail.com
GMAIL_APP_PASSWORD=your-gmail-app-password
SMTP_FROM=hcposts@gmail.com
DEFAULT_RECIPIENT_EMAILS=operator1@example.com,operator2@example.com
```

Optional:

```bash
SEND_EMAIL=false
```

`DEFAULT_RECIPIENT_EMAILS` is a comma-separated list. The operator page no longer asks for an email address; every generated post is sent to these defaults.

`SEND_EMAIL=false` is useful for smoke testing rendering without sending real email.

## Logo Assets

The repository includes the production logo variants:

```text
assets/logo-light.png  # black logo for light frames
assets/logo-dark.png   # white logo for dark frames
```

The generated PNG uses a thin frame and a small top-right logo mark. Phone number and location text are not drawn onto the image.

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DEFAULT_RECIPIENT_EMAILS=operator@example.com SEND_EMAIL=false uvicorn api.render:app --reload
```

Open `http://127.0.0.1:8000` for the local app. The same FastAPI process serves `index.html` and `/api/render`.

## Vercel Deployment

1. Import this repository in Vercel.
2. Add the Gmail environment variables above.
3. Deploy the `main` branch or merge the Codex branch.
4. Visit the generated `*.vercel.app` URL and submit a test post.
