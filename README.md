# 👻 PHANTOM SPINE | Live Signal Bridge v0.2.0

<!-- GLITCHBYTE-VISITOR-BADGE:START -->
[![Page Views](https://hitscounter.dev/api/hit?url=https%3A%2F%2Fgithub.com%2FHellfire13666%2Fphantom-spine-live-signal-2026&label=PAGE%20VIEWS&icon=emoji-smile&color=%23FF1493&style=flat-square)](https://github.com/Hellfire13666/phantom-spine-live-signal-2026)
<!-- GLITCHBYTE-VISITOR-BADGE:END -->

**GlitchByte Phantom Labs** · RosieGlitchbyte · Python 3 · Debian field-tested public-source intelligence and genuine SHA-256 evidence

![Approved Rosie and PHANTOM SPINE official artwork](assets/rosie-phantom-spine-approved.png)

**This is the exact approved Rosie-and-spine artwork, included intact in the public landing page.** Run `index.html` for the branded start hub with real copyable commands, documentation, and field-tested outcomes.

## Verified real functionality

| Engine | What it really does | Debian field result, October 21, 2026 |
| --- | --- | --- |
| Built-in native DNS | HTTPS DNS requests to Google and Cloudflare; real sources and results | **6 actual observations** from 6 usable queries, 0 failed |
| HEXBAZAAR v0.1.2-rc1 adapter | Launches *separately installed* HEXBAZAAR with actual public-provider responses | **113 actual observations** from 4 usable providers |
| RIFTSEAL adapter | Computes and independently cross-checks SHA-256 of a selected **local** file | **PASS**: 8,826 bytes, two matching digests |

Public providers may return zero records, rate limits or timeouts; dated outcomes above are not forecasts. In the DNS field test, two Cloudflare queries returned HTTP 200 but zero accepted DNS observations. **No fabricated data**, no login bypass, no credential collection, no direct target probing, no automatic research-report files.

**Separate dependencies:** HEXBAZAAR and RIFTSEAL are **not** included in this package. Native public DNS works independently. Python 3.11+ recommended; stdlib-only runtime. Debian field-tested; Ubuntu has **not** been independently field-tested.

## 🌹 One-square verified install, no overwrite

After you download **both** versioned files `phantom-spine-live-signal-v0.2.0.zip` and `phantom-spine-live-signal-v0.2.0.sha256` into `~/Downloads`, paste:

```bash
cd "$HOME/Downloads" &&
sha256sum -c phantom-spine-live-signal-v0.2.0.sha256 &&
unzip -tq phantom-spine-live-signal-v0.2.0.zip &&
mkdir -p "$HOME/PhantomLabsLaunchers" &&
test ! -e "$HOME/PhantomLabsLaunchers/phantom-spine-live-signal-v0_2_0" &&
test ! -L "$HOME/PhantomLabsLaunchers/phantom-spine-live-signal-v0_2_0" &&
unzip -q phantom-spine-live-signal-v0.2.0.zip -d "$HOME/PhantomLabsLaunchers" &&
python3 -B "$HOME/PhantomLabsLaunchers/phantom-spine-live-signal-v0_2_0/scripts/verify_package.py" &&
(cd "$HOME/PhantomLabsLaunchers/phantom-spine-live-signal-v0_2_0" && python3 -B -m unittest discover -s tests -v) &&
bash "$HOME/PhantomLabsLaunchers/phantom-spine-live-signal-v0_2_0/INSTALL_LIVE_SHORTCUTS.sh" &&
bash "$HOME/PhantomLabsLaunchers/phantom-spine-live-signal-v0_2_0/OPEN_LIVE_GUIDE.sh"
```

This creates a **new** versioned folder and versioned short command, never overwriting the old RC2, HEXBAZAAR, RIFTSEAL, Master Hub or old desktop icons. The installer preserves any existing same-version desktop shortcut rather than replacing it; use the existing shortcut if already installed.

### Easy forever Start

```bash
"$HOME/.local/bin/phantom-spine-live-v020" start
```

### Easy: real HTTPS DNS

```bash
"$HOME/.local/bin/phantom-spine-live-v020" hunt example.com --engine native --providers dns --timeout 8
```

### Medium: real installed HEXBAZAAR engine

```bash
"$HOME/.local/bin/phantom-spine-live-v020" hunt facebook.com --engine hexbazaar --providers dns,ripe,certspotter,urlscan --timeout 4 --limit 100
```

### Savage: broader public sources (slower, bounded)

```bash
"$HOME/.local/bin/phantom-spine-live-v020" hunt example.com --engine hexbazaar --providers dns,ripe,crtsh,wayback,urlscan,certspotter --timeout 6 --limit 120
```

### Real file evidence using installed RIFTSEAL

```bash
"$HOME/.local/bin/phantom-spine-live-v020" evidence --file "$HOME/PhantomLabsLaunchers/glitchbyte-phantom-labs-master-hub-v0_2_0/index.html" --via riftseal
```

If RIFTSEAL is not installed, replace `--via riftseal` with `--via local`. That computes a genuine independent local SHA-256 without the companion tool. Use `"$HOME/.local/bin/phantom-spine-live-v020" shop` to check whether optional companion files exist; **FOUND is not a live-provider success test**.

## 📦 Package content and verified provenance

- `index.html`: public landing page featuring the *exact owner-approved spine4.png* Rosie artwork, not an AI mock-up of functionality.
- `examples.html`, `connections.html`, `adapter-guide.html`, `troubleshooting.html`: original real executable/adapter instructions with validated flags and genuine source references.
- `spine_live/core.py`: executable real native DNS, real HEXBAZAAR bridge and genuine RIFTSEAL verification; `tests/`: deterministic regression tests, no fabricated public output.
- `INSTALL_LIVE_SHORTCUTS.sh`, `OPEN_LIVE_GUIDE.sh`, `START_PHANTOM_SPINE_LIVE.sh`: version-specific Linux/XFCE entry points.
- `RELEASE_NOTES.md`: actual observed field evidence, including no-data queries and verification limits; `LICENSE-NOTICE.md`: source-available usage/rights terms.
- `MANIFEST.json`: per-file SHA-256 checksums; `scripts/verify_package.py`: standalone read-only integrity check.

The **ZIP + `.sha256`** are two distribution files. The public GitHub release and separate Phantom Backup HQ Installer Vault copy require publication and checksum verification; a local ZIP or page **alone** is not proof those public milestones have occurred.

## Privacy, lawful use, limitations

Your public domain is submitted to the named external DNS providers or the public providers HEXBAZAAR contacts. Only analyze data lawfully available to you; active probes require your authorization. Public-source observations are not proof of current uptime, ownership, misconduct or identity. Do not publicize private reports or secrets. The tools are supplied without guarantees of availability. See [release notes](RELEASE_NOTES.md) and [license notice](LICENSE-NOTICE.md).
