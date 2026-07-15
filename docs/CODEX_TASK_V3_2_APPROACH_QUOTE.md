# Codex Task — V3.2 Homepage: Author Quote, Working Approach, and Audience Additions

## Repository

`proaiexpert/alina-horb-website`

## Goal

Add Alina's author voice and a professionally framed description of her working approach to the Ukrainian and Russian homepages without redesigning the site, overstating qualifications, or weakening the existing safety model.

## Branch and PR

- Create branch: `feature/v32-approach-quote`
- Open one PR to `main`.
- Do not merge automatically.
- Preserve `noindex, nofollow`.

## Files expected

- `index.html`
- `ru/index.html`
- the current versioned homepage stylesheet only if additional styling is necessary
- `docs/PROJECT_SOURCE_OF_TRUTH.md`
- optionally `README.md` only if the feature inventory requires a small factual update

Do not add runtime content injection or a temporary JavaScript/CSS hotfix. The new copy must exist semantically in HTML.

## Ukrainian content

Keep the existing About section structure and portrait. Replace the current short generic quote with:

> Для мене справжня сила — не в тому, щоб завжди долати труднощі наодинці. Іноді вона починається з чесного визнання: мені важко, мені потрібна опора. Віра, близькі люди й уважне ставлення до себе можуть допомогти поступово відновлювати внутрішню цілісність і знаходити власний шлях далі.

Signature:

`Аліна Горб · про внутрішню опору`

Add a compact subsection titled:

`Підхід у роботі`

Use this approved copy:

> У роботі я спираюся на клієнт-центрований підхід — повагу до досвіду людини, її темпу, особистих меж і права самостійно визначати важливі для себе зміни.
>
> Залежно від запиту можу використовувати окремі інструменти гештальт-підходу та метафоричні асоціативні картки. Вони допомагають знаходити слова для переживань, помічати внутрішні реакції та досліджувати ситуацію з різних сторін. Метафоричні картки не є діагностичним тестом і використовуються лише за згодою клієнта.
>
> Якщо для людини важливі питання віри, духовного досвіду, сенсу життя або особистих цінностей, ці теми також можуть бути включені в консультацію — без нав’язування релігійних поглядів і з повагою до світогляду клієнта.

Present the approach as three restrained editorial rows or blocks:

1. `Клієнт-центрований підхід`
2. `Гештальт-інструменти та метафоричні картки`
3. `Віра, цінності та пошук сенсу`

The detailed copy may be split between these rows without changing its meaning.

## Russian content

Use a natural Russian localization, not a literal word-by-word translation.

Quote:

> Для меня настоящая сила — не в том, чтобы всегда преодолевать трудности в одиночку. Иногда она начинается с честного признания: мне тяжело, мне нужна опора. Вера, близкие люди и бережное отношение к себе могут помочь постепенно восстанавливать внутреннюю целостность и находить собственный путь дальше.

Signature:

`Алина Горб · о внутренней опоре`

Subsection title:

`Подход в работе`

Approved copy:

> В работе я опираюсь на клиент-центрированный подход — уважение к опыту человека, его темпу, личным границам и праву самостоятельно определять важные для себя изменения.
>
> В зависимости от запроса я могу использовать отдельные инструменты гештальт-подхода и метафорические ассоциативные карты. Они помогают находить слова для переживаний, замечать внутренние реакции и рассматривать ситуацию с разных сторон. Метафорические карты не являются диагностическим тестом и используются только с согласия клиента.
>
> Если человеку важны вопросы веры, духовного опыта, смысла жизни или личных ценностей, эти темы также могут быть включены в консультацию — без навязывания религиозных взглядов и с уважением к мировоззрению клиента.

Three rows or blocks:

1. `Клиент-центрированный подход`
2. `Гештальт-инструменты и метафорические карты`
3. `Вера, ценности и поиск смысла`

## Audience additions

Add two carefully worded areas without presenting them as diagnoses or exclusive specializations.

UA:

- `Материнство без партнерської підтримки` — психологічна підтримка матерів, які виховують дітей самостійно та переживають виснаження, самотність, перевантаження або складні життєві зміни.
- `Люди старшого віку` — підтримка під час втрат, самотності, змін у здоров’ї, родинних ролях, звичному способі життя або відчутті власної опори.

RU:

- `Материнство без партнерской поддержки` — психологическая поддержка матерей, которые воспитывают детей самостоятельно и переживают истощение, одиночество, перегрузку или сложные жизненные изменения.
- `Люди старшего возраста` — поддержка во время утрат, одиночества, изменений здоровья, семейных ролей, привычного образа жизни или ощущения собственной опоры.

Place these within the existing topics/directions system. Preserve visual rhythm; do not create a large separate demographic section.

## Required safety corrections

- Do not use `перша екстрена допомога / первая экстренная помощь`.
- Preserve the existing wording around primary psychological support during acute stress and the explicit emergency-services boundary.
- Do not claim that Alina is a certified gestalt therapist, transpersonal therapist, clinical psychologist, psychotherapist, religion specialist, or licensed specialist.
- Do not claim that metaphorical cards diagnose, test, reveal the subconscious, or predict anything.
- Do not present faith or religion as mandatory, corrective, or superior to medical/psychological care.
- Do not use claims that every loss contains a lesson or every difficulty makes a person stronger.
- Remove or soften any nearby unsupported claim such as regular supervision if it is not confirmed in the current source of truth.

## Design constraints

- Preserve Premium Editorial Sanctuary V3.1.
- Keep the approved Hero and About portraits unchanged.
- No new stock images.
- No new large section unless necessary; integrate within About and the existing topics list.
- Keep copy readable and compact on mobile.
- No horizontal carousel.
- No heavy animation.
- Preserve reduced-motion support.

## QA

Run the asset validator and browser QA for UA/RU at:

- 390 px
- 768 px
- 1024 px
- 1366 px
- 1440 px

Acceptance:

- broken images: 0
- asset 404: 0
- console errors: 0
- horizontal overflow: 0
- one H1 per page
- no duplicate IDs
- quote is readable and does not dominate the page
- approach blocks stack correctly on mobile
- UA/RU language links remain correct
- form, mobile menu, floating CTA and footer remain functional
- `noindex, nofollow` remains present

## Return

Return only:

- PR URL
- head commit SHA
- changed-file list
- validation results
- screenshots or exact reason screenshots were unavailable
- any remaining factual blocker
