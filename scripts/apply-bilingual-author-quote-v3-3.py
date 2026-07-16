#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

replacements = {
    ROOT / "index.html": (
        '<blockquote class="editorial-quote editorial-quote--author"><p>Для мене справжня сила — не в тому, щоб завжди долати труднощі наодинці. Іноді вона починається з чесного визнання: мені важко, мені потрібна опора. Віра, близькі люди й уважне ставлення до себе можуть допомогти поступово відновлювати внутрішню цілісність і знаходити власний шлях далі.</p><footer>Аліна Горб · про внутрішню опору</footer></blockquote>',
        '<blockquote class="editorial-quote editorial-quote--author"><p>Часом життя ставить перед нами випробування. Знайди в собі ресурс, щоб їх прийняти.</p><p>У кожній складності прихований урок, у кожній втраті — можливість для нового усвідомлення.</p><p>Відкрий внутрішнє джерело, яке веде тебе вперед, і пам’ятай: справжня сила народжується не лише в перемогах, а й у здатності зберігати віру, любов і гармонію навіть у найважчі моменти.</p><p>Кожне випробування — це крок до глибшого пізнання себе й свого призначення.</p><footer>Аліна Горб · про внутрішню опору</footer></blockquote>',
    ),
    ROOT / "ru/index.html": (
        '<blockquote class="editorial-quote editorial-quote--author"><p>Для меня настоящая сила — не в том, чтобы всегда преодолевать трудности в одиночку. Иногда она начинается с честного признания: мне тяжело, мне нужна опора. Вера, близкие люди и бережное отношение к себе могут помочь постепенно восстанавливать внутреннюю целостность и находить собственный путь дальше.</p><footer>Алина Горб · о внутренней опоре</footer></blockquote>',
        '<blockquote class="editorial-quote editorial-quote--author"><p>Порой жизнь ставит перед нами испытания. Найди в себе ресурс, чтобы их принять.</p><p>В каждой трудности скрыт урок, в каждой потере — возможность для нового осознания.</p><p>Открой внутренний источник, который ведёт тебя вперёд, и помни: настоящая сила рождается не только в победах, но и в способности сохранять веру, любовь и гармонию даже в самые трудные моменты.</p><p>Каждое испытание — это шаг к более глубокому познанию себя и своего предназначения.</p><footer>Алина Горб · о внутренней опоре</footer></blockquote>',
    ),
}

for path, (old, new) in replacements.items():
    text = path.read_text(encoding="utf-8")
    if new in text:
        continue
    if old not in text:
        raise SystemExit(f"Expected quote block not found in {path.relative_to(ROOT)}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

ua = (ROOT / "index.html").read_text(encoding="utf-8")
ru = (ROOT / "ru/index.html").read_text(encoding="utf-8")
assert "Часом життя ставить перед нами випробування" in ua
assert "Кожне випробування — це крок" in ua
assert "Порой жизнь ставит перед нами испытания" in ru
assert "Каждое испытание — это шаг" in ru
print("Bilingual author quote updated and validated")
