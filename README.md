<div align="center">

# MeowBox

**Free, no-ads file sharing & hosting with direct links**

[![Website](https://img.shields.io/badge/website-meowbox.dpdns.org-4c9aff?style=flat-square&logo=cloudflare)](https://meowbox.dpdns.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Built with Cloudflare Workers](https://img.shields.io/badge/Cloudflare-Workers-F38020?style=flat-square&logo=cloudflare)](https://workers.cloudflare.com)
[![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)](https://meowbox.dpdns.org)

[Website](https://meowbox.dpdns.org) • [FAQ](https://meowbox.dpdns.org/faq) • [Tools & API](https://meowbox.dpdns.org/tools) • [Safety](https://meowbox.dpdns.org/safety) • [Legal](https://meowbox.dpdns.org/legal) • [Contact](https://meowbox.dpdns.org/contact)

</div>

---

## What MeowBox Is

MeowBox is a **free file hosting service** that gives you a direct, hotlinkable link for every upload. No ads, no trackers, no paywalls, no required accounts. Upload a file (up to 25 MB), get a link like `https://meowbox.dpdns.org/f/abc123xyz`, and share it anywhere — Discord, forums, blogs, chats, `<img>` tags, `<video>` embeds.

## Why It Exists

Most file hosts either throttle free users, force signups, inject ads, or expire links after a few days. MeowBox was built to be the exception: anonymous by default, permanent links unless you choose expiry, and completely free.

## Features at a Glance

| Feature | Details |
|---------|---------|
| **Direct links** | Every upload → `/f/xxxxxx` URL that works everywhere |
| **Anonymous uploads** | No email, no signup, no login required |
| **Expiring links** | Permanent by default, or auto-delete after 2 h / 24 h / 2 d / 7 d (returns `410 Gone`) |
| **Albums & delete control** | Free account adds dashboard, albums, one-click deletion |
| **Malware scanning** | Every upload checked against MalwareBazaar + VirusTotal before serving; known malware blocked & blacklisted |
| **All file types** | Images, video, audio, PDF, archives up to 25 MB (GIFs capped at 20 MB) |
| **REST API** | Single `POST /user/api.php` endpoint, one `reqtype` per action |
| **Zero tracking** | No ads, no analytics, no third-party scripts, no data sold |
| **Explicit limits** | All caps published on the [Tools page](https://meowbox.dpdns.org/tools) |

---

## How It Works (30-Second Overview)

1. **Upload** — drag & drop a file on the homepage, or `POST /user/api.php` with `reqtype=fileupload`.
2. **Get a link** — receive a short direct URL (`/f/xxxxxx`).
3. **Share** — the link serves the file with correct `Content-Type`, CORS headers, and cache hints. No intermediate pages, no CAPTCHAs.

**Under the hood** (high-level, no implementation code):
- Cloudflare Worker handles every request at the edge.
- Metadata (file hash, owner, expiry, storage location) lives in a Cloudflare D1 database.
- File blobs are stored in **two tiers**: primary edge KV for small/short-lived payloads, and a secondary remote object store for larger or permanent files. Exact provider details are intentionally not published to reduce abuse surface.
- Expired files are purged by a cron (`*/15 * * * *`) that also cleans the database and cache.
- Every upload is scanned against MalwareBazaar (SHA-256) and optionally VirusTotal before being stored or served. Scanning failures fail open (file accepted) to avoid availability loss.
- Rate limits protect the service: 60 uploads/hour/IP, 25 views/min/IP, signup/login throttling.

---

## Quick Start

### Web (no account)

1. Open [meowbox.dpdns.org](https://meowbox.dpdns.org)
2. Drag a file or click to select
3. Copy the direct link — done

### Free account (dashboard, albums, deletion)

1. Click **Register** → username (3–32 chars, lowercase/digits/_), password (≥ 8 chars), optional email
2. Log in → dashboard at `/manage`
4. Create albums, delete files, set custom expiries

### API (one endpoint, one `reqtype`)

```bash
# Upload a file
curl -X POST https://meowbox.dpdns.org/user/api.php \
  -F "reqtype=fileupload" \
  -F "fileToUpload=@photo.jpg"

# Upload from a URL
curl -X POST https://meowbox.dpdns.org/user/api.php \
  -F "reqtype=urlupload" \
  -F "url=https://example.com/video.mp4" \
  -F "ttl=172800"   # 2 days in seconds (0 = permanent)

# Delete your files (needs userhash from upload response or account)
curl -X POST https://meowbox.dpdns.org/user/api.php \
  -F "reqtype=deletefiles" \
  -F "userhash=your_userhash" \
  -F "files=abc123xyz def456uvw"
```

Full API reference → **[docs/API.md](docs/API.md)**  
All limits → **[docs/LIMITS.md](docs/LIMITS.md)**

---

## File Types & Limits

| Category | Limit |
|----------|-------|
| Max file size | 25 MB |
| GIF size | 20 MB (use WebM for animation) |
| Expiry options | 2 h / 24 h / 2 d / 7 d, or permanent (default) |
| Banned extensions | `.exe, .scr, .cpl, .jar, .msi, .msix, .bat, .cmd, .vbs, .vbe, .wsf, .wsh, .ps1, .psm1, .hta, .lnk, .reg, .apk, .appx, .xll, .doc, .docm, .docx, .dot, .dotx, .htaccess, .php, .phtml` |
| Upload rate | 60 req/hour/IP (anti-abuse) |
| View rate | 25 req/min/IP → then 5,000 req/hour/IP |
| Signup rate | 5 req/hour/IP |
| Login attempts | 20 req/15 min/IP, 8 per username/15 min |
| Username | 3–32 chars, `a-z 0-9 _` |
| Password | min 8 chars |
| Session TTL | 30 days (HttpOnly, Secure, SameSite=Lax cookie) |

Complete limits table → **[docs/LIMITS.md](docs/LIMITS.md)**

---

## Security & Privacy

- **HTTPS everywhere**, 1-year HSTS, strict CSP on every page
- **Zero third-party scripts** — no analytics, no trackers, no pixels
- **Uploader IP** retained only for anti-abuse (malware/DMCA reports), documented on [Legal page](https://meowbox.dpdns.org/legal)
- **Malware scan** on every upload (MalwareBazaar SHA-256 + optional VirusTotal), cached 30 days
- **Magic-byte checks** block MZ (PE) and ELF executables
- **Expired files** return `410 Gone` and are purged from storage
- **Delete anonymous files** with the `userhash` returned at upload time

Security policy → **[SECURITY.md](SECURITY.md)**  
Privacy details → **[docs/PRIVACY.md](docs/PRIVACY.md)**

---

## Documentation Index

| Document | Description |
|----------|-------------|
| [README.md](README.md) | This file — overview, quick start, links |
| [docs/HOW-IT-WORKS.md](docs/HOW-IT-WORKS.md) | Architecture, request lifecycle, storage tiers, expiry, scanning |
| [docs/API.md](docs/API.md) | Complete API reference with `reqtype` table, fields, curl examples, error codes |
| [docs/LIMITS.md](docs/LIMITS.md) | Every limit with rationale and edge-case behavior |
| [docs/FAQ.md](docs/FAQ.md) | 20+ frequently asked questions |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Tech stack, data flow, storage tiers, cron, security boundaries |
| [docs/PRIVACY.md](docs/PRIVACY.md) | Data collected, retention, deletion rights, contact |
| [docs/SEO.md](docs/SEO.md) | Sitemap, IndexNow, JSON-LD schema, Bing/Google guidance |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Planned features and milestones |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | How to deploy your own instance (bindings, secrets, wrangler) |
| [docs/SUPPORT.md](docs/SUPPORT.md) | Help, abuse/DMCA reporting, contact |

---

## Architecture at a Glance

```text
Client → Cloudflare Edge (Worker)
            │
            ├─ D1 (SQLite) → metadata: file hash, owner, expiry, storage ref
            ├─ KV (edge)   → small/short-lived blobs (≤ 25 MB, TTL ≤ 7 d)
            ├─ Remote store → larger/permanent blobs
            ├─ KV cache    → 30-day malware scan results
            └─ Cron (15m)  → purge expired, clean DB, cache
```

Detailed architecture → **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**

---

## Roadmap

See **[docs/ROADMAP.md](docs/ROADMAP.md)** for planned features (WebP auto-conversion, folder upload, WebDAV, client SDKs, etc.).

---

## Contributing

This repository contains **documentation only** — the service source code is not published here.  
Contributions to docs, issue reports, and feature suggestions are very welcome.

→ **[CONTRIBUTING.md](CONTRIBUTING.md)** — ground rules, PR checklist, reporting security issues

---

## Security Issues

**Do not open a public issue.** Report privately via GitHub Security Advisories:

https://github.com/BhagattJii/meowbox/security/advisories/new

→ **[SECURITY.md](SECURITY.md)** — full policy, scope, expected response time

---

## License

MIT — see **[LICENSE](LICENSE)**.

---

## Credits & Contact

Built by **BhagattJii** — [GitHub](https://github.com/BhagattJii) • [Instagram](https://www.instagram.com/i.lakshyy) • [Email](mailto:meowboxteam@gmail.com)

Stack: Cloudflare Workers + D1 + KV + Assets  
Hosted on: `meowbox.dpdns.org` (custom domain on Cloudflare)

---

*If MeowBox helped you, a ⭐ on this repo is appreciated.*