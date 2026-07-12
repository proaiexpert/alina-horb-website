# Preview Release Checklist

Before merging `feat/bilingual-ua-ru-v3` into `main`:

- [x] PR #6 closed without merge.
- [x] Ukrainian page is primary at `/`.
- [x] Russian page is available at `/ru/`.
- [x] Language switch works in header and footer.
- [x] UA and RU pages use their corresponding approved logo.
- [x] Practice wording uses 2016.
- [x] Khust, Germany, city, address, phone, and WhatsApp are not published.
- [x] Online is the primary format.
- [x] In-person consultation is described only as possible by prior agreement.
- [x] Price remains outside the hero.
- [x] Email and localized mailto form work.
- [x] Telegram username is not guessed and remains disabled.
- [x] Public redacted diploma remains the only diploma asset used.
- [x] GitHub Pages workflow publishes `index.html`, `ru/`, and `assets/` directly from the repository.
- [x] Deployment has no Google Drive or ZIP dependency.
- [x] Both preview pages use `noindex, nofollow`.
- [x] Responsive and functional QA completed for both languages.

After merge:

- [ ] Verify `https://proaiexpert.github.io/alina-horb-website/`.
- [ ] Verify `https://proaiexpert.github.io/alina-horb-website/ru/`.
- [ ] Recheck both language switches on the deployed project URL.
- [ ] Recheck network requests and browser console on the deployed preview.

Before production indexing:

- [ ] Confirm Telegram username.
- [ ] Publish and link the privacy policy.
- [ ] Connect and verify `alinahorb.com`.
- [ ] Remove `noindex, nofollow` in a separate production commit.
