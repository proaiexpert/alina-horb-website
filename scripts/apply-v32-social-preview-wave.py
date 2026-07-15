#!/usr/bin/env python3
"""Generate bilingual social cards and apply the approved Hero/metadata wave.

This script is deterministic and idempotent. It uses the already approved Hero
portrait without retouching the subject; only crop, resize, colour management,
compression and restrained sharpening are applied.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PORTRAIT = ROOT / "assets/images/portrait/alina-horb-hero-v3-1-desktop.jpg"
SOCIAL_DIR = ROOT / "assets/images/social"
UA_IMAGE = SOCIAL_DIR / "alina-horb-og-ua-v1.jpg"
RU_IMAGE = SOCIAL_DIR / "alina-horb-og-ru-v1.jpg"

WIDTH, HEIGHT = 1200, 630
IVORY = "#f4efe7"
IVORY_SOFT = "#faf7f1"
STONE = "#e8ded3"
SAGE_DEEP = "#66705f"
TERRACOTTA = "#c6533f"
GRAPHITE = "#2f302d"
MUTED = "#686963"

SERIF_PATHS = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf",
)
SANS_PATHS = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
)
SANS_BOLD_PATHS = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
)


def font(paths: Iterable[str], size: int) -> ImageFont.FreeTypeFont:
    for candidate in paths:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    raise FileNotFoundError(f"No usable font found in: {tuple(paths)}")


def fit_font(draw: ImageDraw.ImageDraw, text: str, paths: Iterable[str], start: int, min_size: int, max_width: int) -> ImageFont.FreeTypeFont:
    for size in range(start, min_size - 1, -1):
        candidate = font(paths, size)
        if draw.textbbox((0, 0), text, font=candidate)[2] <= max_width:
            return candidate
    return font(paths, min_size)


def create_card(*, language: str, output: Path) -> None:
    if not PORTRAIT.exists():
        raise FileNotFoundError(PORTRAIT)

    canvas = Image.new("RGB", (WIDTH, HEIGHT), IVORY)
    draw = ImageDraw.Draw(canvas)

    # Editorial structure: restrained text field on the left, approved portrait on the right.
    draw.rectangle((0, 0, WIDTH, 14), fill=TERRACOTTA)
    draw.rectangle((0, 14, 690, HEIGHT), fill=IVORY)
    draw.line((82, 518, 630, 518), fill="#cfc3b7", width=2)

    with Image.open(PORTRAIT) as source:
        source = source.convert("RGB")
        # Slight colour normalization only; no face/body/hair/book alteration.
        source = ImageEnhance.Color(source).enhance(0.96)
        source = ImageEnhance.Contrast(source).enhance(1.02)
        portrait = ImageOps.fit(
            source,
            (550, HEIGHT - 14),
            method=Image.Resampling.LANCZOS,
            centering=(0.50, 0.45),
        )
        portrait = portrait.filter(ImageFilter.UnsharpMask(radius=1.0, percent=55, threshold=3))

    canvas.paste(portrait, (650, 14))

    # Soft transition keeps the composition premium rather than looking like a hard split template.
    blend = Image.new("RGBA", (150, HEIGHT - 14), (0, 0, 0, 0))
    blend_px = blend.load()
    ivory_rgb = (244, 239, 231)
    for x in range(blend.width):
        alpha = int(255 * (1 - x / (blend.width - 1)))
        for y in range(blend.height):
            blend_px[x, y] = (*ivory_rgb, alpha)
    canvas.paste(blend, (620, 14), blend)

    if language == "uk":
        name = "Аліна Горб"
        role = "ПСИХОЛОГ"
        line = "Онлайн-консультації українською та російською"
        domain = "alinahorb.com"
        marker = "UA"
    elif language == "ru":
        name = "Алина Горб"
        role = "ПСИХОЛОГ"
        line = "Онлайн-консультации на русском и украинском"
        domain = "alinahorb.com/ru/"
        marker = "RU"
    else:
        raise ValueError(language)

    name_font = fit_font(draw, name, SERIF_PATHS, 64, 54, 500)
    role_font = font(SANS_BOLD_PATHS, 21)
    line_font = fit_font(draw, line, SANS_PATHS, 24, 19, 510)
    domain_font = font(SANS_BOLD_PATHS, 18)
    marker_font = font(SANS_BOLD_PATHS, 16)

    draw.text((82, 118), name, font=name_font, fill=GRAPHITE)
    draw.text((85, 212), role, font=role_font, fill=TERRACOTTA)
    draw.text((82, 286), line, font=line_font, fill=SAGE_DEEP)
    draw.text((82, 545), domain, font=domain_font, fill=GRAPHITE)

    draw.rounded_rectangle((557, 72, 624, 110), radius=17, fill=IVORY_SOFT, outline=TERRACOTTA, width=2)
    draw.text((590, 91), marker, font=marker_font, fill=TERRACOTTA, anchor="mm")

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, "JPEG", quality=88, optimize=True, progressive=True, subsampling=1)


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected exactly one {label}; found {count}")
    return text.replace(old, new, 1)


def update_ua() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")

    old_og = '''  <meta property="og:type" content="website">\n  <meta property="og:locale" content="uk_UA">\n  <meta property="og:title" content="Аліна Горб — психолог">\n  <meta property="og:description" content="Коли всередині надто багато, не обов’язково справлятися наодинці.">\n  <meta property="og:url" content="https://alinahorb.com/">\n  <meta property="og:image" content="https://proaiexpert.github.io/alina-horb-website/assets/images/portrait/alina-horb-hero-v3-1-desktop.jpg">\n  <meta property="og:image:width" content="900">\n  <meta property="og:image:height" content="1350">\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:title" content="Аліна Горб — психолог">\n  <meta name="twitter:description" content="Психологічна підтримка українською та російською мовами.">\n  <meta name="twitter:image" content="https://proaiexpert.github.io/alina-horb-website/assets/images/portrait/alina-horb-hero-v3-1-desktop.jpg">'''
    new_og = '''  <meta property="og:type" content="website">\n  <meta property="og:site_name" content="Аліна Горб — психолог">\n  <meta property="og:locale" content="uk_UA">\n  <meta property="og:locale:alternate" content="ru_RU">\n  <meta property="og:title" content="Аліна Горб — психолог">\n  <meta property="og:description" content="Психологічна підтримка українською та російською. Онлайн; очно — за попереднім погодженням.">\n  <meta property="og:url" content="https://alinahorb.com/">\n  <meta property="og:image" content="https://alinahorb.com/assets/images/social/alina-horb-og-ua-v1.jpg">\n  <meta property="og:image:secure_url" content="https://alinahorb.com/assets/images/social/alina-horb-og-ua-v1.jpg">\n  <meta property="og:image:type" content="image/jpeg">\n  <meta property="og:image:width" content="1200">\n  <meta property="og:image:height" content="630">\n  <meta property="og:image:alt" content="Аліна Горб — психологічні консультації українською та російською">\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:title" content="Аліна Горб — психолог">\n  <meta name="twitter:description" content="Психологічна підтримка українською та російською. Онлайн; очно — за попереднім погодженням.">\n  <meta name="twitter:image" content="https://alinahorb.com/assets/images/social/alina-horb-og-ua-v1.jpg">\n  <meta name="twitter:image:alt" content="Аліна Горб — психологічні консультації українською та російською">'''
    text = replace_once(text, old_og, new_og, label="UA social metadata block")
    text = replace_once(
        text,
        '<h1 id="hero-title"><span>Коли всередині надто багато,</span><span>не обов’язково справлятися наодинці.</span></h1>',
        '<h1 id="hero-title"><span>Психологічна підтримка,</span><span>коли особливо важко</span></h1>',
        label="UA Hero H1",
    )
    text = replace_once(
        text,
        '<p class="hero-intro">Аліна — психолог для людей різного віку, пар і сімей. Формат роботи з неповнолітніми узгоджується окремо. Консультації українською та російською під час стресу, кризи, емоційного виснаження й складних змін. Онлайн; очно — за попереднім погодженням.</p>',
        '<p class="hero-intro">Коли переживань стає надто багато, не обов’язково залишатися з ними наодинці.</p>',
        label="UA Hero supporting text",
    )
    path.write_text(text, encoding="utf-8")


def update_ru() -> None:
    path = ROOT / "ru/index.html"
    text = path.read_text(encoding="utf-8")

    social_pattern = re.compile(
        r'  <meta property="og:type" content="website"><meta property="og:locale" content="ru_RU">\n'
        r'  <meta property="og:title" content="Алина Горб — психолог"><meta property="og:description" content="Когда внутри слишком много, не обязательно справляться в одиночку\."><meta property="og:url" content="https://alinahorb\.com/ru/">\n'
        r'  <meta property="og:image" content="https://proaiexpert\.github\.io/alina-horb-website/assets/images/portrait/alina-horb-hero-v3-1-desktop\.jpg"><meta property="og:image:width" content="900"><meta property="og:image:height" content="1350">\n'
        r'  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Алина Горб — психолог"><meta name="twitter:description" content="Психологическая поддержка на русском и украинском языках\."><meta name="twitter:image" content="https://proaiexpert\.github\.io/alina-horb-website/assets/images/portrait/alina-horb-hero-v3-1-desktop\.jpg">'
    )
    new_social = '''  <meta property="og:type" content="website">\n  <meta property="og:site_name" content="Алина Горб — психолог">\n  <meta property="og:locale" content="ru_RU">\n  <meta property="og:locale:alternate" content="uk_UA">\n  <meta property="og:title" content="Алина Горб — психолог">\n  <meta property="og:description" content="Психологическая поддержка на русском и украинском. Онлайн; очно — по предварительному согласованию.">\n  <meta property="og:url" content="https://alinahorb.com/ru/">\n  <meta property="og:image" content="https://alinahorb.com/assets/images/social/alina-horb-og-ru-v1.jpg">\n  <meta property="og:image:secure_url" content="https://alinahorb.com/assets/images/social/alina-horb-og-ru-v1.jpg">\n  <meta property="og:image:type" content="image/jpeg">\n  <meta property="og:image:width" content="1200">\n  <meta property="og:image:height" content="630">\n  <meta property="og:image:alt" content="Алина Горб — психологические консультации на русском и украинском">\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:title" content="Алина Горб — психолог">\n  <meta name="twitter:description" content="Психологическая поддержка на русском и украинском. Онлайн; очно — по предварительному согласованию.">\n  <meta name="twitter:image" content="https://alinahorb.com/assets/images/social/alina-horb-og-ru-v1.jpg">\n  <meta name="twitter:image:alt" content="Алина Горб — психологические консультации на русском и украинском">'''
    text, count = social_pattern.subn(new_social, text, count=1)
    if count != 1:
        raise RuntimeError(f"Expected exactly one RU social metadata block; found {count}")

    text = replace_once(
        text,
        '<h1 id="hero-title"><span>Когда внутри слишком много,</span><span>не обязательно справляться в одиночку.</span></h1>',
        '<h1 id="hero-title"><span>Психологическая поддержка,</span><span>когда особенно трудно</span></h1>',
        label="RU Hero H1",
    )
    text = replace_once(
        text,
        '<p class="hero-intro">Алина — психолог для людей разного возраста, пар и семей. Формат работы с несовершеннолетними согласуется отдельно. Консультации на русском и украинском во время стресса, кризиса, эмоционального истощения и сложных перемен. Онлайн; очно — по предварительному согласованию.</p>',
        '<p class="hero-intro">Когда переживаний становится слишком много, не обязательно оставаться с ними в одиночку.</p>',
        label="RU Hero supporting text",
    )
    path.write_text(text, encoding="utf-8")


def update_deploy_workflow() -> None:
    path = ROOT / ".github/workflows/deploy-pages.yml"
    text = path.read_text(encoding="utf-8")
    old = "      - name: Validate production asset references\n        run: python3 scripts/validate-assets.py"
    new = "      - name: Validate production asset references\n        run: |\n          python3 scripts/validate-assets.py\n          python3 scripts/validate-social-previews.py"
    if old in text:
        text = text.replace(old, new, 1)
        path.write_text(text, encoding="utf-8")
    elif "python3 scripts/validate-social-previews.py" not in text:
        raise RuntimeError("Could not update deployment validation step")


def main() -> None:
    SOCIAL_DIR.mkdir(parents=True, exist_ok=True)
    create_card(language="uk", output=UA_IMAGE)
    create_card(language="ru", output=RU_IMAGE)
    update_ua()
    update_ru()
    update_deploy_workflow()
    print(f"Generated {UA_IMAGE.relative_to(ROOT)} ({UA_IMAGE.stat().st_size} bytes)")
    print(f"Generated {RU_IMAGE.relative_to(ROOT)} ({RU_IMAGE.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
