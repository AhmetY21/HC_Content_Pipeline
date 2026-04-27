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
```

Optional:

```bash
DEFAULT_RECIPIENT_EMAIL=operator@example.com
SEND_EMAIL=false
```

`SEND_EMAIL=false` is useful for smoke testing rendering without sending real email.

## Logo Assets

The renderer looks for these files in order:

```text
assets/logo-light.png
assets/logo-dark.png
assets/logo.png
```

If no logo is present, the backend draws a simple H&C fallback mark so the app still works after deployment. Replace it with transparent PNG logo files when H&C provides final artwork.

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
SEND_EMAIL=false uvicorn api.render:app --reload
```

Open `http://127.0.0.1:8000` for the local app. The same FastAPI process serves `index.html` and `/api/render`.

## Vercel Deployment

1. Import this repository in Vercel.
2. Add the Gmail environment variables above.
3. Deploy the `main` branch or merge the Codex branch.
4. Visit the generated `*.vercel.app` URL and submit a test post.
