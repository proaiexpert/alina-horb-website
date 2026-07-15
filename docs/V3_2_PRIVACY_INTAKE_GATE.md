# V3.2 Privacy and intake release gate

This wave establishes a conservative bilingual privacy baseline while public indexing remains disabled.

## Canonical public contact

- `hello@alinahorb.com`
- Telegram remains the primary direct-contact option.

## First-contact data minimization

The form requests only a preferred name, reply contact, channel, language, meeting format and a short message. It must not request diagnoses, medical documents, identity documents, payment-card data or detailed crisis information.

## Safety boundary

The website, form, email and direct messages are not emergency services and do not guarantee an immediate response. Immediate danger must be directed to local emergency or crisis services in the person’s country.

## Technical state

- UA policy: `/privacy/`
- RU policy: `/ru/privacy/`
- configurable endpoint remains empty until a provider/account is approved;
- mailto fallback uses `hello@alinahorb.com`;
- honeypot and minimum-interaction-time checks reduce basic automated spam;
- `noindex, nofollow` remains active.
