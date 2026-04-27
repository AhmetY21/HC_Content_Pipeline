from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageOps, UnidentifiedImageError

try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
except Exception:
    pass

from .content import CATEGORIES


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"
FRAME_MARGIN = 34
LOGO_SIZE = 150
LOGO_PADDING = 18

FRAME_COLORS = {
    "light": {
        "frame": "#F5F5EE",
        "text": "#1A1A1A",
        "phone": "#00945F",
        "border": (0, 0, 0, 34),
        "shadow": (0, 0, 0, 26),
    },
    "dark": {
        "frame": "#0E0E18",
        "text": "#E2E2EE",
        "phone": "#00E09A",
        "border": (255, 255, 255, 18),
        "shadow": (255, 255, 255, 18),
    },
}


class RenderError(ValueError):
    pass


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def _rounded_image(image: Image.Image, radius: int) -> Image.Image:
    rounded = Image.new("RGBA", image.size, (0, 0, 0, 0))
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, image.width, image.height), radius=radius, fill=255)
    rounded.paste(image.convert("RGBA"), (0, 0), mask)
    return rounded


def _load_logo(mode: str) -> Image.Image | None:
    candidates = [
        ASSET_DIR / f"logo-{mode}.png",
        ASSET_DIR / "logo.png",
        ASSET_DIR / "logo-light.png",
    ]
    for path in candidates:
        if path.exists():
            logo = Image.open(path).convert("RGBA")
            logo.thumbnail((LOGO_SIZE, LOGO_SIZE), Image.Resampling.LANCZOS)
            return logo
    return None


def compose_post(photo_bytes: bytes, category: str, frame_mode: str) -> bytes:
    if category not in CATEGORIES:
        raise RenderError("Geçersiz kategori seçildi.")
    if frame_mode not in FRAME_COLORS:
        raise RenderError("Geçersiz çerçeve modu seçildi.")

    try:
        source = Image.open(BytesIO(photo_bytes))
        source = ImageOps.exif_transpose(source)
    except (UnidentifiedImageError, OSError):
        raise RenderError("Fotoğraf okunamadı, tekrar yükleyin.")

    source.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
    source = source.convert("RGB")

    width, height = CATEGORIES[category].size
    colors = FRAME_COLORS[frame_mode]
    frame_rgb = _hex_to_rgb(colors["frame"])
    canvas = Image.new("RGB", (width, height), frame_rgb)

    inner_x = FRAME_MARGIN
    inner_y = FRAME_MARGIN
    inner_w = width - (FRAME_MARGIN * 2)
    inner_h = height - (FRAME_MARGIN * 2)

    cropped = ImageOps.fit(
        source,
        (inner_w, inner_h),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.4),
    )
    cropped = ImageEnhance.Sharpness(cropped).enhance(1.04)
    photo = _rounded_image(cropped, radius=16)

    shadow = Image.new("RGBA", (inner_w + 4, inner_h + 4), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((2, 2, inner_w + 2, inner_h + 2), radius=18, fill=colors["shadow"])
    canvas.paste(shadow, (inner_x - 2, inner_y - 2), shadow)
    canvas.paste(photo, (inner_x, inner_y), photo)

    border_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border_layer)
    border_draw.rounded_rectangle(
        (inner_x, inner_y, inner_x + inner_w, inner_y + inner_h),
        radius=16,
        outline=colors["border"],
        width=2,
    )
    canvas = Image.alpha_composite(canvas.convert("RGBA"), border_layer).convert("RGB")
    draw = ImageDraw.Draw(canvas)

    logo = _load_logo(frame_mode)
    if logo:
        logo_layer = Image.new("RGBA", (LOGO_SIZE + 18, LOGO_SIZE + 18), (0, 0, 0, 0))
        logo_bg = Image.new("RGBA", logo_layer.size, frame_rgb + (220,))
        logo_layer.alpha_composite(logo_bg)
        logo_layer.alpha_composite(logo, ((logo_layer.width - logo.width) // 2, (logo_layer.height - logo.height) // 2))
        logo_x = width - FRAME_MARGIN - LOGO_PADDING - logo_layer.width
        logo_y = FRAME_MARGIN + LOGO_PADDING
        canvas.paste(logo_layer, (logo_x, logo_y), logo_layer)

    output = BytesIO()
    canvas.save(output, format="PNG", optimize=True)
    return output.getvalue()
