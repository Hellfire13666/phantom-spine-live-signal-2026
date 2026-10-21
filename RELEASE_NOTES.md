# PHANTOM SPINE Live Signal v0.2.0 · Field-verified release notes

**Version:** v0.2.0 · **Field system:** Debian XFCE/Trixie · **Field-test date:** October 21, 2026

## Real outcomes (observed, not synthetic)

- HEXBAZAAR v0.1.2-rc1 adapter invoked against public domain `facebook.com`; 113 unique observations, 4 usable providers, 0 provider notices; output and provenance streamed; `[SAVE OFF]`.
- Native HTTPS DNS queries of `example.com`: 6 genuine observations (2 A, 2 AAAA, 2 NS), 6 usable DNS query responses, 0 failed; total observed 11 seconds. Google's MX and Cloudflare's A/AAAA requests returned zero accepted observations despite HTTP 200 and DNS 0. A successful transport query is not necessarily a returned record.
- Local RIFTSEAL bridge on existing Master Hub HTML file: SHA-256 `b6dcac8c87d2f54cfc27c61a1ff12e5914789016985d428b89f4bd44a078ae4f`, 8,826 bytes, independent calculations matched. This local file test made no internet request.
- Offline package unit tests verify result parsing, no-data handling, provider errors and compatibility behavior. They **do not** replace actual owner Debian checks above. Provider observations can change at any time.

## Public release package

- Uses the user's selected **exact `spine4.png` Rosie + glowing-spine artwork**, copied unchanged into `assets/rosie-phantom-spine-approved.png` as the public page's full-width hero and available inside this ZIP.
- New versioned install folder and **`phantom-spine-live-v020`** starter. Keeps existing RC1/RC2 and installed tools untouched.
- Real copy buttons, professionally branded local homepage, Easy/Medium/Savage examples, compatibility and troubleshooting pages.
- Public-source HTTPS requests only for `hunt`; RIFTSEAL evidence checks use local files. No automatic report saving; no login or credential access.
- Released code is source-available with rights reserved (see `LICENSE-NOTICE.md`), **not** OSI open source.

## Support limits

Field-tested on the owner's Debian machine; independent native and HEXBAZAAR runs passed on that environment. **Ubuntu is not separately field-tested**. Installed HEXBAZAAR and RIFTSEAL are **optional separate tools, not bundled** and may have separate license terms and output behavior. A domain observation cannot prove a host is currently online, a person's identity, ownership or wrongdoing.

**Reminder:** A locally built ZIP is not automatically a public GitHub Release or a Phantom Vault backup. Confirm that both are physically present before advertising their URLs.
