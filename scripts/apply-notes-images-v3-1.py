#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

IMAGES = {
    "first": {
        "file": "alina-horb-note-first-consultation-v3.webp",
        "uk": "Два крісла у спокійному світлому просторі для першої консультації",
        "ru": "Два кресла в спокойном светлом пространстве для первой консультации",
    },
    "conversation": {
        "file": "alina-horb-note-conversation-v3.webp",
        "uk": "Відкритий нотатник як образ початку складної розмови",
        "ru": "Открытый блокнот как образ начала трудного разговора",
    },
    "observation": {
        "file": "alina-horb-note-observation-v3.webp",
        "uk": "Нотатник і ручка як образ уважного спостереження за власним станом",
        "ru": "Блокнот и ручка как образ внимательного наблюдения за своим состоянием",
    },
    "transition": {
        "file": "alina-horb-note-transition-v3.webp",
        "uk": "Коробка, мапа і ключ як образ переїзду та відновлення опори",
        "ru": "Коробка, карта и ключ как образ переезда и восстановления опоры",
    },
}

SLUGS = {
    "first-consultation": "first",
    "how-to-start-the-conversation": "conversation",
    "when-coping-stops-helping": "observation",
    "stress-relocation-and-lost-support": "transition",
}

HOME_PAGES = {
    Path("index.html"): ("uk", "assets/"),
    Path("ru/index.html"): ("ru", "../assets/"),
}

HUB_PAGES = {
    Path("notes/index.html"): ("uk", "../assets/"),
    Path("ru/notes/index.html"): ("ru", "../../assets/"),
}

ARTICLE_PAGES = {}
for slug, key in SLUGS.items():
    ARTICLE_PAGES[Path("notes") / slug / "index.html"] = ("uk", "../../assets/", key)
    ARTICLE_PAGES[Path("ru/notes") / slug / "index.html"] = ("ru", "../../../assets/", key)


def picture(asset_prefix: str, key: str, lang: str, eager: bool = False) -> str:
    item = IMAGES[key]
    return (
        f'<picture><img src="{asset_prefix}images/notes/{item["file"]}" '
        f'width="1200" height="800" loading="{"eager" if eager else "lazy"}" '
        f'decoding="async" alt="{item[lang]}"></picture>'
    )


def inject_assets(text: str, asset_prefix: str) -> str:
    css_href = f'{asset_prefix}css/site.notes-images.v3.css?v=3.1'
    if css_href not in text:
        text = text.replace("</head>", f'  <link rel="stylesheet" href="{css_href}">\n</head>', 1)
    return text


def add_photo_classes(opening: str, key: str) -> str:
    match = re.search(r'class="([^"]*)"', opening)
    if not match:
        return opening
    classes = match.group(1).split()
    for value in ("note-photo", f"note-photo--{key}"):
        if value not in classes:
            classes.append(value)
    return opening[: match.start(1)] + " ".join(classes) + opening[match.end(1) :]


def replace_identity(text: str, key: str, markup: str) -> str:
    pattern = re.compile(
        rf'(<a\b[^>]*class="[^"]*note-identity--{re.escape(key)}[^"]*"[^>]*>).*?(</a>)',
        re.S,
    )

    def replacement(match: re.Match) -> str:
        return add_photo_classes(match.group(1), key) + markup + match.group(2)

    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"Could not replace {key} identity")
    return text


def replace_feature(text: str, class_name: str, number_class: str, markup: str) -> str:
    pattern = re.compile(
        rf'(<a\b[^>]*class="[^"]*{re.escape(class_name)}[^"]*"[^>]*>).*?'
        rf'(<span\b[^>]*class="[^"]*{re.escape(number_class)}[^"]*"[^>]*>.*?</span>)(</a>)',
        re.S,
    )
    text, count = pattern.subn(lambda m: m.group(1) + markup + m.group(2) + m.group(3), text, count=1)
    if count != 1:
        raise SystemExit(f"Could not replace feature media {class_name}")
    return text


def set_meta_content(text: str, selector_name: str, selector_value: str, content: str) -> str:
    pattern = re.compile(
        rf'(<meta\s+{re.escape(selector_name)}="{re.escape(selector_value)}"\s+content=")[^"]*(">)',
        re.I,
    )
    return pattern.sub(lambda m: m.group(1) + content + m.group(2), text)


def apply_home(path: Path, lang: str, asset_prefix: str) -> None:
    full = ROOT / path
    text = inject_assets(full.read_text(encoding="utf-8"), asset_prefix)
    text = replace_feature(text, "home-note-feature-media", "home-note-index", picture(asset_prefix, "first", lang))
    for key in ("conversation", "observation", "transition"):
        text = replace_identity(text, key, picture(asset_prefix, key, lang))
    full.write_text(text, encoding="utf-8")


def apply_hub(path: Path, lang: str, asset_prefix: str) -> None:
    full = ROOT / path
    text = inject_assets(full.read_text(encoding="utf-8"), asset_prefix)
    text = replace_feature(text, "notes-hub-feature-media", "notes-hub-feature-number", picture(asset_prefix, "first", lang, True))
    for key in ("conversation", "observation", "transition"):
        text = replace_identity(text, key, picture(asset_prefix, key, lang))
    absolute = "https://alinahorb.com/assets/images/notes/" + IMAGES["first"]["file"]
    text = set_meta_content(text, "property", "og:image", absolute)
    text = set_meta_content(text, "name", "twitter:image", absolute)
    text = set_meta_content(text, "property", "og:image:width", "1200")
    text = set_meta_content(text, "property", "og:image:height", "800")
    full.write_text(text, encoding="utf-8")


def apply_article(path: Path, lang: str, asset_prefix: str, key: str) -> None:
    full = ROOT / path
    text = inject_assets(full.read_text(encoding="utf-8"), asset_prefix)
    markup = picture(asset_prefix, key, lang, True)
    pattern = re.compile(
        r'(<figure\b[^>]*class="[^"]*article-hero-visual[^"]*"[^>]*>\s*)<picture>.*?</picture>',
        re.S,
    )
    text, count = pattern.subn(lambda m: m.group(1) + markup, text, count=1)
    if count != 1:
        raise SystemExit(f"Could not replace article hero in {path}")

    body_pattern = re.compile(r'<body\s+class="([^"]*article-template-v32[^"]*)"([^>]*)>')
    if "data-note=" not in text:
        text, body_count = body_pattern.subn(lambda m: f'<body class="{m.group(1)}" data-note="{key}"{m.group(2)}>', text, count=1)
        if body_count != 1:
            raise SystemExit(f"Could not set data-note in {path}")

    absolute = "https://alinahorb.com/assets/images/notes/" + IMAGES[key]["file"]
    for selector_name, selector_value in (
        ("property", "og:image"),
        ("property", "og:image:secure_url"),
        ("name", "twitter:image"),
    ):
        text = set_meta_content(text, selector_name, selector_value, absolute)
    text = set_meta_content(text, "property", "og:image:width", "1200")
    text = set_meta_content(text, "property", "og:image:height", "800")
    text = re.sub(r'("image"\s*:\s*")[^"]*(")', lambda m: m.group(1) + absolute + m.group(2), text, count=1)
    full.write_text(text, encoding="utf-8")


def main() -> None:
    for path, (lang, asset_prefix) in HOME_PAGES.items():
        apply_home(path, lang, asset_prefix)
    for path, (lang, asset_prefix) in HUB_PAGES.items():
        apply_hub(path, lang, asset_prefix)
    for path, (lang, asset_prefix, key) in ARTICLE_PAGES.items():
        apply_article(path, lang, asset_prefix, key)
    print("Static Notes imagery applied to 12 RU/UA pages")


if __name__ == "__main__":
    main()
