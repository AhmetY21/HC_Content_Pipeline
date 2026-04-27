from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, UnidentifiedImageError

try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
except Exception:
    pass

from .content import CATEGORIES


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"
FONT_DIRS = [
    ROOT / "assets" / "fonts",
    Path("/System/Library/Fonts"),
    Path("/Library/Fonts"),
]

BRAND_LINE_1 = "📞 0541 970 09 11  ·  Şaşmaz Oto Sanayi"
BRAND_LINE_2 = "H&C OTOMOTİV  ·  7/7 AÇIK"

FRAME_COLORS = {
    "light": {
        "frame": "#F5F5EE",
        "text": "#1A1A1A",
        "phone": "#00945F",
        "border": (0, 0, 0, 34),
        "shadow": (0, 0, 0, 26),
        "gradient_delta": -10,
    },
    "dark": {
        "frame": "#0E0E18",
        "text": "#E2E2EE",
        "phone": "#00E09A",
        "border": (255, 255, 255, 18),
        "shadow": (255, 255, 255, 18),
        "gradient_delta": 10,
    },
}


class RenderError(ValueError):
    pass


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def _adjust_rgb(rgb: tuple[int, int, int], delta: int) -> tuple[int, int, int]:
    return tuple(max(0, min(255, channel + delta)) for channel in rgb)


def _interpolate(a: tuple[int, int, int], b: tuple[int, int, int], ratio: float) -> tuple[int, int, int]:
    return tuple(round(a[i] + (b[i] - a[i]) * ratio) for i in range(3))


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "JetBrainsMono-Bold.ttf" if bold else "JetBrainsMono-Regular.ttf",
        "Outfit-Bold.ttf" if bold else "Outfit-Regular.ttf",
        "Montserrat-VariableFont_wght.ttf",
        "Arial Unicode.ttf",
        "Arial.ttf",
    ]
    for directory in FONT_DIRS:
        for candidate in candidates:
            path = directory / candidate
            if path.exists():
                return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


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
            logo.thumbnail((140, 140), Image.Resampling.LANCZOS)
            return logo
    return None


def _draw_fallback_logo(canvas: Image.Image, xy: tuple[int, int], mode: str) -> None:
    draw = ImageDraw.Draw(canvas)
    x, y = xy
    colors = FRAME_COLORS[mode]
    accent = _hex_to_rgb(colors["phone"])
    text = _hex_to_rgb(colors["text"])
    draw.rounded_rectangle((x, y, x + 140, y + 140), radius=28, outline=accent, width=4)
    draw.text((x + 23, y + 39), "H&C", fill=text, font=_font(38, bold=True))
    draw.rectangle((x + 28, y + 98, x + 112, y + 104), fill=accent)


def _draw_text_with_emoji_fallback(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fill: tuple[int, int, int],
    font: ImageFont.ImageFont,
) -> None:
    try:
        draw.text(xy, text, fill=fill, font=font)
    except UnicodeEncodeError:
        draw.text(xy, text.replace("📞 ", ""), fill=fill, font=font)


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
    draw = ImageDraw.Draw(canvas)

    inner_x = 60
    inner_y = 60
    inner_w = width - 120
    inner_h = height - 280

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

    accent = _hex_to_rgb(colors["phone"])
    draw.rounded_rectangle((30, 30, 34, 70), radius=2, fill=accent)

    logo = _load_logo(frame_mode)
    logo_x = width - 170
    logo_y = 30
    if logo:
        canvas.paste(logo, (logo_x + (140 - logo.width) // 2, logo_y + (140 - logo.height) // 2), logo)
    else:
        _draw_fallback_logo(canvas, (logo_x, logo_y), frame_mode)

    strip_y = height - 160
    start = frame_rgb
    end = _adjust_rgb(frame_rgb, colors["gradient_delta"])
    for offset in range(160):
        ratio = offset / 159
        draw.line((0, strip_y + offset, width, strip_y + offset), fill=_interpolate(start, end, ratio))

    phone_font = _font(34, bold=True)
    brand_font = _font(31, bold=True)
    text_rgb = _hex_to_rgb(colors["text"])
    phone_rgb = _hex_to_rgb(colors["phone"])
    _draw_text_with_emoji_fallback(draw, (70, strip_y + 33), BRAND_LINE_1, phone_rgb, phone_font)
    draw.text((70, strip_y + 89), BRAND_LINE_2, fill=text_rgb, font=brand_font)

    output = BytesIO()
    canvas.save(output, format="PNG", optimize=True)
    return output.getvalue()

