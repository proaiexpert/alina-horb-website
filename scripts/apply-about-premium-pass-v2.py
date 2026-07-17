#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = ROOT / "about/index.html"
RU = ROOT / "ru/about/index.html"
CSS = ROOT / "assets/css/site.about.v1.css"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"Pattern not found: {label}")
    return text.replace(old, new, 1)


ua = UA.read_text(encoding="utf-8")
ru = RU.read_text(encoding="utf-8")
css = CSS.read_text(encoding="utf-8")

ua = replace_once(ua,
'''<h1 id="profile-title"><span>Психологічна підтримка,</span><span>у якій можна залишатися собою</span></h1>''',
'''<h1 id="profile-title"><span>Психологічна підтримка,</span><span>коли внутрішню опору доводиться знаходити наново</span></h1>''', "UA hero title")
ua = replace_once(ua,
'''<p class="profile-lead">Я працюю з людьми, які переживають стрес, кризу, втрату звичної опори, переїзд, тривогу або складні життєві зміни.</p>
        <p>Для мене консультація — це не місце, де людина повинна одразу знати правильні відповіді. Це простір, у якому можна поступово зрозуміти, що відбувається, знайти слова для свого досвіду та визначити посильні наступні кроки.</p>''',
'''<p class="profile-lead">Я працюю з людьми, які переживають стрес, кризу, втрату звичної опори, переїзд, тривогу або інші складні життєві зміни.</p>
        <p>Для мене консультація — це простір, у якому можна спокійніше побачити, що відбувається, знайти слова для свого досвіду й визначити посильні наступні кроки.</p>''', "UA hero copy")
ua = replace_once(ua,
'''<p class="profile-opening">Психологічну практику я веду з 2016 року. Працюю з людьми різного віку, індивідуальними, парними та сімейними зверненнями; формат роботи з неповнолітніми узгоджується окремо.</p>
          <p>У центрі моєї професійної уваги — ситуації, у яких людині особливо складно зберігати відчуття внутрішньої опори: гострий або тривалий стрес, наслідки війни, вимушене переміщення, переїзд, тривожні стани, панічні прояви, втрати, труднощі у стосунках та інші складні зміни.</p>
          <p>Я не вважаю, що до психолога потрібно приходити з уже сформульованим запитом. Іноді достатньо почати з простого: «Мені важко, і я хочу зрозуміти, що зі мною відбувається».</p>''',
'''<p class="profile-opening">Практикую з 2016 року. Працюю з індивідуальними, парними та сімейними зверненнями; формат роботи з неповнолітніми узгоджується окремо.</p>
          <p>Найчастіше це ситуації, у яких людині важко зберігати внутрішню опору: гострий або тривалий стрес, наслідки війни, вимушене переміщення, переїзд, тривожні стани, панічні прояви, втрати та труднощі у стосунках.</p>
          <p>Не обов’язково приходити вже з чітким формулюванням. Іноді достатньо почати з простого: «Мені важко, і я хочу зрозуміти, що зі мною відбувається».</p>''', "UA path copy")
ua = replace_once(ua,
'''<article data-reveal><span>01</span><h3>Не вимагати «правильного» запиту</h3><p>На першій зустрічі можна не знати, з чого почати. Ми можемо разом визначити, що зараз потребує найбільшої уваги.</p></article>
          <article data-reveal><span>02</span><h3>Не нав’язувати готових рішень</h3><p>Я не вирішую за людину, як їй жити або що обирати. Моє завдання — допомогти краще побачити ситуацію, власні реакції, потреби та можливості.</p></article>
          <article data-reveal><span>03</span><h3>Поважати темп і межі</h3><p>Клієнт має право не відповідати на запитання, відмовитися від вправи або зупинити обговорення теми, до якої поки не готовий.</p></article>
          <article data-reveal><span>04</span><h3>Бути чесною щодо можливостей</h3><p>Якщо запит потребує медичної, психіатричної, кризової або іншої спеціалізованої допомоги, я поясню це й пораджу відповідного фахівця.</p></article>''',
'''<article data-reveal><span>01</span><h3>Не вимагати «правильного» запиту</h3><p>На першій зустрічі можна не знати, з чого почати. Ми можемо разом визначити, що зараз справді потребує уваги.</p></article>
          <article data-reveal><span>02</span><h3>Не нав’язувати готових рішень</h3><p>Я не вирішую за людину, як їй жити. Моє завдання — допомогти краще побачити ситуацію, власні реакції та можливі наступні кроки.</p></article>
          <article data-reveal><span>03</span><h3>Поважати темп і межі</h3><p>Клієнт має право не відповідати на запитання, відмовитися від вправи або зупинити тему, до якої поки не готовий.</p></article>
          <article data-reveal><span>04</span><h3>Бути чесною щодо можливостей</h3><p>Коли запит потребує медичної, психіатричної, кризової або іншої спеціалізованої допомоги, я прямо пояснюю це й рекомендую відповідного фахівця.</p></article>''', "UA position copy")
ua = replace_once(ua,
'''<article data-reveal><span class="method-index">01</span><div><h3>Клієнт-центрований підхід</h3><p>У роботі я спираюся на повагу до досвіду людини, її темпу, особистих меж і права самостійно визначати важливі для себе зміни. У консультації немає завдання відповідати очікуванням психолога або демонструвати «правильну» поведінку.</p></div></article>
          <article data-reveal><span class="method-index">02</span><div><h3>Гештальт-інструменти</h3><p>Залежно від запиту можу використовувати окремі інструменти гештальт-підходу. Вони допомагають помічати емоції, тілесні реакції, потреби та способи взаємодії з іншими людьми.</p></div></article>
          <article data-reveal><span class="method-index">03</span><div><h3>Метафоричні асоціативні картки</h3><p>Картки можуть допомогти знайти слова для переживань або подивитися на ситуацію з іншого боку. Вони не є діагностичним тестом, не передбачають майбутнє і використовуються лише за згодою клієнта.</p></div></article>
          <article data-reveal><span class="method-index">04</span><div><h3>Віра, цінності та пошук сенсу</h3><p>Якщо для людини важливі питання віри, духовного досвіду, особистих цінностей або сенсу життя, вони можуть бути включені в консультацію. Релігійні переконання не нав’язуються, а світогляд клієнта залишається пріоритетом.</p></div></article>''',
'''<article data-reveal><span class="method-index">01</span><div><h3>Клієнт-центрований підхід</h3><p>У роботі я спираюся на повагу до досвіду людини, її темпу, особистих меж і права самостійно визначати важливі для себе зміни.</p></div></article>
          <article data-reveal><span class="method-index">02</span><div><h3>Гештальт-інструменти</h3><p>За потреби можу використовувати окремі інструменти гештальт-підходу. Вони допомагають краще помічати емоції, тілесні реакції та способи взаємодії з іншими.</p></div></article>
          <article data-reveal><span class="method-index">03</span><div><h3>Метафоричні асоціативні картки</h3><p>Картки можуть допомогти знайти слова для переживань або подивитися на ситуацію з іншого боку. Вони не є діагностичним тестом і використовуються лише за згодою клієнта.</p></div></article>
          <article data-reveal><span class="method-index">04</span><div><h3>Віра, цінності та пошук сенсу</h3><p>Якщо для людини важливі питання віри, духовного досвіду, особистих цінностей або сенсу життя, ці теми можуть бути включені в консультацію — без нав’язування поглядів і з повагою до світогляду клієнта.</p></div></article>''', "UA methods copy")
ua = replace_once(ua,
'''<p>Освіта дає професійну основу, але не скасовує необхідності уважно ставитися до складності кожного випадку, перевіряти межі власної компетенції та за потреби рекомендувати іншого фахівця.</p>''',
'''<p>Освіта дає професійну основу, але в роботі для мене не менш важливі уважність до складності кожної ситуації, межі компетенції та чесність із клієнтом.</p>''', "UA education note")
ua = replace_once(ua,
'''</section>

    <section class="profile-methods section-block" id="methods" aria-labelledby="methods-title">''',
'''</section>

    <section class="profile-editorial section-block" aria-labelledby="editorial-title">
      <div class="page-shell profile-editorial-layout">
        <div class="profile-editorial-voice" data-reveal>
          <p class="section-kicker">Професійна інтонація</p>
          <h2 id="editorial-title">Повернути можливість спокійно відчувати, помічати й розуміти</h2>
          <blockquote class="profile-editorial-quote">
            <p>Для мене важливо не квапити людину з висновками та рішеннями. Іноді спочатку потрібно повернути можливість спокійно відчувати, помічати й розуміти те, що відбувається.</p>
            <footer>Аліна Горб · професійна позиція</footer>
          </blockquote>
        </div>
        <figure class="profile-editorial-figure" data-reveal>
          <img src="../assets/images/notes/alina-horb-note-observation-v3.webp" width="1800" height="1200" loading="lazy" decoding="async" alt="Відкритий блокнот і олівець у спокійному світлому просторі">
          <figcaption>Спокійний простір для розмови, зосередження й нотаток.</figcaption>
        </figure>
      </div>
    </section>

    <section class="profile-methods section-block" id="methods" aria-labelledby="methods-title">''', "UA editorial block")

ru = replace_once(ru,
'''<h1 id="profile-title"><span>Психологическая поддержка,</span><span>в которой можно оставаться собой</span></h1>''',
'''<h1 id="profile-title"><span>Психологическая поддержка,</span><span>когда внутреннюю опору приходится находить заново</span></h1>''', "RU hero title")
ru = replace_once(ru,
'''<p class="profile-lead">Я работаю с людьми, которые переживают стресс, кризис, потерю привычной опоры, переезд, тревогу или сложные жизненные изменения.</p>
        <p>Для меня консультация — это не место, где человек обязан сразу знать правильные ответы. Это пространство, в котором можно постепенно разобраться в происходящем, найти слова для своего опыта и определить посильные следующие шаги.</p>''',
'''<p class="profile-lead">Я работаю с людьми, которые переживают стресс, кризис, потерю привычной опоры, переезд, тревогу или другие сложные жизненные изменения.</p>
        <p>Для меня консультация — это пространство, в котором можно спокойнее увидеть происходящее, найти слова для своего опыта и определить посильные следующие шаги.</p>''', "RU hero copy")
ru = replace_once(ru,
'''<p class="profile-opening">Психологическую практику я веду с 2016 года. Работаю с людьми разного возраста, индивидуальными, парными и семейными обращениями; формат работы с несовершеннолетними согласуется отдельно.</p>
          <p>В центре моего профессионального внимания — ситуации, в которых человеку особенно трудно сохранять ощущение внутренней опоры: острый или продолжительный стресс, последствия войны, вынужденное перемещение, переезд, тревожные состояния, панические проявления, потери, трудности в отношениях и другие сложные изменения.</p>
          <p>Я не считаю, что к психологу нужно приходить с уже сформулированным запросом. Иногда достаточно начать с простого: «Мне тяжело, и я хочу понять, что со мной происходит».</p>''',
'''<p class="profile-opening">Практикую с 2016 года. Работаю с индивидуальными, парными и семейными обращениями; формат работы с несовершеннолетними согласуется отдельно.</p>
          <p>Чаще всего это ситуации, в которых человеку трудно сохранять внутреннюю опору: острый или продолжительный стресс, последствия войны, вынужденное перемещение, переезд, тревожные состояния, панические проявления, потери и трудности в отношениях.</p>
          <p>Необязательно приходить уже с чётко сформулированным запросом. Иногда достаточно начать с простого: «Мне тяжело, и я хочу понять, что со мной происходит».</p>''', "RU path copy")
ru = replace_once(ru,
'''<article data-reveal><span>01</span><h3>Не требовать «правильного» запроса</h3><p>На первой встрече можно не знать, с чего начать. Мы можем вместе определить, что сейчас требует наибольшего внимания.</p></article>
          <article data-reveal><span>02</span><h3>Не навязывать готовых решений</h3><p>Я не решаю за человека, как ему жить или что выбирать. Моя задача — помочь лучше увидеть ситуацию, собственные реакции, потребности и возможности.</p></article>
          <article data-reveal><span>03</span><h3>Уважать темп и границы</h3><p>Клиент имеет право не отвечать на вопрос, отказаться от упражнения или остановить обсуждение темы, к которой пока не готов.</p></article>
          <article data-reveal><span>04</span><h3>Быть честной относительно возможностей</h3><p>Когда запрос требует медицинской, психиатрической, кризисной или другой специализированной помощи, я объясню это и порекомендую соответствующего специалиста.</p></article>''',
'''<article data-reveal><span>01</span><h3>Не требовать «правильного» запроса</h3><p>На первой встрече можно не знать, с чего начать. Мы можем вместе определить, что сейчас действительно требует внимания.</p></article>
          <article data-reveal><span>02</span><h3>Не навязывать готовых решений</h3><p>Я не решаю за человека, как ему жить. Моя задача — помочь лучше увидеть ситуацию, собственные реакции и возможные следующие шаги.</p></article>
          <article data-reveal><span>03</span><h3>Уважать темп и границы</h3><p>Клиент имеет право не отвечать на вопрос, отказаться от упражнения или остановить тему, к которой пока не готов.</p></article>
          <article data-reveal><span>04</span><h3>Быть честной относительно возможностей</h3><p>Когда запрос требует медицинской, психиатрической, кризисной или другой специализированной помощи, я прямо объясняю это и рекомендую соответствующего специалиста.</p></article>''', "RU position copy")
ru = replace_once(ru,
'''<article data-reveal><span class="method-index">01</span><div><h3>Клиент-центрированный подход</h3><p>В работе я опираюсь на уважение к опыту человека, его темпу, личным границам и праву самостоятельно определять важные для себя изменения. В консультации нет задачи соответствовать ожиданиям психолога или демонстрировать «правильное» поведение.</p></div></article>
          <article data-reveal><span class="method-index">02</span><div><h3>Гештальт-инструменты</h3><p>В зависимости от запроса я могу применять отдельные инструменты гештальт-подхода. Они помогают замечать эмоции, телесные реакции, потребности и способы взаимодействия с другими людьми.</p></div></article>
          <article data-reveal><span class="method-index">03</span><div><h3>Метафорические ассоциативные карты</h3><p>Карты могут помочь найти слова для переживаний или посмотреть на ситуацию с другой стороны. Они не являются диагностическим тестом, не предсказывают будущее и используются только с согласия клиента.</p></div></article>
          <article data-reveal><span class="method-index">04</span><div><h3>Вера, ценности и поиск смысла</h3><p>Когда для человека важны вопросы веры, духовного опыта, личных ценностей или смысла жизни, они могут быть включены в консультацию. Религиозные убеждения не навязываются, а мировоззрение клиента остаётся приоритетом.</p></div></article>''',
'''<article data-reveal><span class="method-index">01</span><div><h3>Клиент-центрированный подход</h3><p>В работе я опираюсь на уважение к опыту человека, его темпу, личным границам и праву самостоятельно определять важные для себя изменения.</p></div></article>
          <article data-reveal><span class="method-index">02</span><div><h3>Гештальт-инструменты</h3><p>При необходимости я могу использовать отдельные инструменты гештальт-подхода. Они помогают лучше замечать эмоции, телесные реакции и способы взаимодействия с другими.</p></div></article>
          <article data-reveal><span class="method-index">03</span><div><h3>Метафорические ассоциативные карты</h3><p>Карты могут помочь найти слова для переживаний или посмотреть на ситуацию с другой стороны. Они не являются диагностическим тестом и используются только с согласия клиента.</p></div></article>
          <article data-reveal><span class="method-index">04</span><div><h3>Вера, ценности и поиск смысла</h3><p>Когда для человека важны вопросы веры, духовного опыта, личных ценностей или смысла жизни, эти темы могут быть включены в консультацию — без навязывания взглядов и с уважением к мировоззрению клиента.</p></div></article>''', "RU methods copy")
ru = replace_once(ru,
'''<p>Образование даёт профессиональную основу, но не отменяет необходимости внимательно относиться к сложности каждого случая, учитывать границы собственной компетенции и при необходимости рекомендовать другого специалиста.</p>''',
'''<p>Образование даёт профессиональную основу, но в работе для меня не менее важны внимательность к сложности каждой ситуации, границы компетенции и честность с клиентом.</p>''', "RU education note")
ru = replace_once(ru,
'''</section>

    <section class="profile-methods section-block" id="methods" aria-labelledby="methods-title">''',
'''</section>

    <section class="profile-editorial section-block" aria-labelledby="editorial-title">
      <div class="page-shell profile-editorial-layout">
        <div class="profile-editorial-voice" data-reveal>
          <p class="section-kicker">Профессиональная интонация</p>
          <h2 id="editorial-title">Вернуть возможность спокойно чувствовать, замечать и понимать</h2>
          <blockquote class="profile-editorial-quote">
            <p>Для меня важно не торопить человека с выводами и решениями. Иногда сначала нужно вернуть возможность спокойно чувствовать, замечать и понимать то, что происходит.</p>
            <footer>Алина Горб · профессиональная позиция</footer>
          </blockquote>
        </div>
        <figure class="profile-editorial-figure" data-reveal>
          <img src="../../assets/images/notes/alina-horb-note-observation-v3.webp" width="1800" height="1200" loading="lazy" decoding="async" alt="Открытый блокнот и карандаш в спокойном светлом пространстве">
          <figcaption>Спокойное пространство для разговора, сосредоточенности и заметок.</figcaption>
        </figure>
      </div>
    </section>

    <section class="profile-methods section-block" id="methods" aria-labelledby="methods-title">''', "RU editorial block")

css = replace_once(css,
'''  background:
    radial-gradient(circle at 82% 8%, rgba(135, 146, 127, .11), transparent 25rem),
    var(--ivory);''',
'''  background:
    radial-gradient(circle at 82% 8%, rgba(135, 146, 127, .11), transparent 25rem),
    linear-gradient(180deg, rgba(255,255,255,.3), rgba(255,255,255,0) 32rem),
    var(--ivory);''', "CSS page background")
css = replace_once(css, '  line-height: 1.78;\n}\n\n.profile-hero-copy .profile-lead', '  line-height: 1.72;\n}\n\n.profile-hero-copy .profile-lead', "CSS hero copy")
css = replace_once(css,
'''.profile-method-list p {
  max-width: 720px;
  margin: 0;
  color: var(--muted);
  font-size: 16px;
  line-height: 1.82;
}''',
'''.profile-method-list p {
  max-width: 720px;
  margin: 0;
  color: var(--muted);
  font-size: 16px;
  line-height: 1.72;
}''', "CSS methods copy")
css = replace_once(css,
'''.profile-education {
  border-block: 1px solid var(--line);
  background: linear-gradient(120deg, var(--stone) 0 43%, var(--ivory-soft) 43% 100%);
}''',
'''.profile-education {
  border-block: 1px solid var(--line);
  background:
    radial-gradient(circle at 14% 16%, rgba(135, 146, 127, .12), transparent 20rem),
    linear-gradient(180deg, rgba(255,255,255,.46), rgba(255,255,255,.08)),
    var(--stone);
}''', "CSS education background")
css = replace_once(css,
'''  border: 1px solid rgba(47,48,45,.2);
  padding: 18px;
  background: rgba(255,255,255,.58);
  box-shadow: 0 28px 70px rgba(47,48,45,.12);
  transition: transform .3s var(--ease), box-shadow .3s ease;''',
'''  border: 1px solid rgba(47,48,45,.16);
  padding: 22px;
  background: rgba(255,255,255,.82);
  box-shadow: 0 20px 50px rgba(47,48,45,.08);
  transition: transform .3s var(--ease), box-shadow .3s ease, border-color .3s ease;''', "CSS diploma frame")
css = replace_once(css,
'''.profile-diploma a:hover {
  transform: translateY(-5px) rotate(-.3deg);
  box-shadow: 0 36px 82px rgba(47,48,45,.16);
}''',
'''.profile-diploma a:hover {
  transform: translateY(-4px);
  border-color: rgba(47,48,45,.26);
  box-shadow: 0 26px 60px rgba(47,48,45,.12);
}''', "CSS diploma hover")
css = replace_once(css,
'''  margin: 34px 0 24px;
  border-left: 2px solid var(--terracotta);
  padding: 2px 0 2px 24px;''',
'''  margin: 32px 0 24px;
  border-left: 1px solid rgba(198,83,63,.55);
  padding: 2px 0 2px 22px;''', "CSS education note")
css = replace_once(css, '.education-note p { margin: 0; color: var(--muted); line-height: 1.8; }', '.education-note p { margin: 0; color: var(--muted); line-height: 1.74; }', "CSS education text")
css = replace_once(css, '.format-copy p { margin-bottom: 20px; font-size: 16px; line-height: 1.82; }', '.format-copy p { margin-bottom: 20px; font-size: 16px; line-height: 1.74; }', "CSS format text")
css = replace_once(css, '.profile-final p { max-width: 630px; color: rgba(250,247,241,.7); font-size: 16px; line-height: 1.8; }', '.profile-final p { max-width: 630px; color: rgba(250,247,241,.7); font-size: 16px; line-height: 1.74; }', "CSS final text")
css = replace_once(css, '.profile-final-action p { margin-bottom: 12px; }', '.profile-final-action p { margin-bottom: 10px; }', "CSS final spacing")
css = replace_once(css,
'''  .profile-education { background: linear-gradient(180deg, var(--stone) 0 46%, var(--ivory-soft) 46% 100%); }''',
'''  .profile-education {
    background:
      linear-gradient(180deg, rgba(255,255,255,.36), rgba(255,255,255,.06)),
      var(--stone);
  }''', "CSS mobile education")
css = replace_once(css, '.profile-methods { background: var(--ivory); }', '''.profile-editorial {
  border-block: 1px solid var(--line);
  background: linear-gradient(180deg, rgba(250,247,241,.8), rgba(244,239,231,.78));
}

.profile-editorial-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.02fr) minmax(300px, .98fr);
  gap: clamp(44px, 7vw, 102px);
  align-items: center;
}

.profile-editorial-voice h2 {
  max-width: 760px;
  margin-bottom: 28px;
  font-size: clamp(44px, 4.8vw, 68px);
  line-height: .96;
  letter-spacing: -.02em;
}

.profile-editorial-quote { max-width: 720px; margin: 0; }

.profile-editorial-quote p {
  margin: 0;
  color: var(--graphite);
  font-family: var(--serif);
  font-size: clamp(34px, 3.5vw, 52px);
  font-style: italic;
  line-height: 1.12;
}

.profile-editorial-quote footer {
  margin-top: 22px;
  color: var(--muted);
  font-size: 13px;
  letter-spacing: .03em;
  text-transform: uppercase;
}

.profile-editorial-figure { width: 100%; margin: 0; }

.profile-editorial-figure img {
  width: 100%;
  aspect-ratio: 4 / 3;
  display: block;
  object-fit: cover;
  border-radius: 26px;
  box-shadow: 0 24px 64px rgba(47,48,45,.1);
}

.profile-editorial-figure figcaption {
  margin-top: 14px;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.6;
}

.profile-methods { background: var(--ivory); }''', "CSS editorial section")
css = replace_once(css,
'''  .profile-final-inner {
    grid-template-columns: minmax(0, 1fr);
    gap: 42px;
  }''',
'''  .profile-final-inner,
  .profile-editorial-layout {
    grid-template-columns: minmax(0, 1fr);
    gap: 42px;
  }''', "CSS editorial mobile grid")
css = replace_once(css,
'''  .profile-method-list article { grid-template-columns: 42px minmax(0, 1fr); gap: 12px; }
  .profile-method-list h3''',
'''  .profile-method-list article { grid-template-columns: 42px minmax(0, 1fr); gap: 12px; }
  .profile-editorial-quote p { font-size: clamp(30px, 7.2vw, 40px); }
  .profile-method-list h3''', "CSS editorial mobile type")

UA.write_text(ua, encoding="utf-8")
RU.write_text(ru, encoding="utf-8")
CSS.write_text(css, encoding="utf-8")
print("Applied premium About page pass to UA, RU and CSS")
