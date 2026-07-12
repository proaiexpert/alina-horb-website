# Proposed PR Description

## Summary

- Makes Ukrainian the primary homepage at `/`.
- Adds a complete Russian version at `/ru/`.
- Adds working relative language switches and localized logos.
- Adds localized contacts and a temporary mailto form.
- Keeps Telegram disabled until its username is confirmed.
- Updates Pages deployment to publish both routes directly from repository files.

## QA

Both languages were checked at 320, 360, 375, 390, 430, 768, 1024, 1280, and 1440 px. No horizontal overflow, broken images, duplicate IDs, console errors, or runtime errors were found.

## Safety

- No Google Drive or ZIP dependency.
- No private portrait or diploma sources.
- No city, address, phone, Germany, or Khust.
- Preview remains `noindex, nofollow`.
- PR #6 is closed without merge.
- Main remains unchanged.
