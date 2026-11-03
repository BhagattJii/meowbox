<div align="center">

# MeowBox

**Free, ad-free file hosting with direct links.**

[![Website](https://img.shields.io/badge/website-meowbox.dpdns.org-4c9aff?style=flat-square)](https://meowbox.dpdns.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)](https://meowbox.dpdns.org)

[Website](https://meowbox.dpdns.org) · [FAQ](https://meowbox.dpdns.org/faq) · [Tools & API](https://meowbox.dpdns.org/tools) · [Safety](https://meowbox.dpdns.org/safety) · [Legal](https://meowbox.dpdns.org/legal) · [Contact](https://meowbox.dpdns.org/contact)

</div>

---

## What is MeowBox?

A free file hosting service that gives you a **direct, hotlinkable link** for every upload. No ads, no trackers, no paywalls, no required accounts.

Upload a file (up to 25 MB), get a link like `https://meowbox.dpdns.org/f/abc123xyz`, and share it anywhere — Discord, forums, blogs, chats, `<img>` tags, `<video>` embeds.

---

## Why MeowBox?

Most file hosts throttle free users, force signups, inject ads, or expire links after a few days. MeowBox was built to be the exception: **anonymous by default, permanent links unless you choose expiry, completely free.**

---

## Features

| Feature | Details |
|---------|---------|
| **Direct links** | Every upload → `/f/xxxxxx` URL that works everywhere |
| **Anonymous uploads** | No email, no signup, no login required |
| **Expiring links** | Permanent by default, or auto-delete after 2 h / 24 h / 2 d / 7 d (returns `410 Gone`) |
| **Albums & delete control** | Free account adds dashboard, albums, one-click deletion |
| **Malware scanning** | Every upload checked before serving; malware blocked & blacklisted |
| **All file types** | Images, video, audio, PDF, archives up to 25 MB (GIFs capped at 20 MB) |
| **REST API** | Single `POST /user/api.php` endpoint, one `reqtype` per action |
| **Zero tracking** | No ads, no analytics, no third-party scripts, no data sold |

---

## Quick Start

### Web (no account)

1. Open [meowbox.dpdns.org](https://meowbox.dpdns.org)
2. Drag a file or click to select
3. Copy the direct link — done

### Free account (dashboard, albums, deletion)

1. Click **Register** → username, password, optional email
2. Log in → dashboard at `/manage`
3. Create albums, delete files, set custom expiries

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

Full API reference → **[docs/api.md](docs/api.md)**  
All limits → **[docs/limits.md](docs/limits.md)**

---

## Limits

| Category | Limit |
|----------|-------|
| Max file size | 25 MB |
| GIF size | 20 MB (use WebM for animation) |
| Expiry options | 2 h / 24 h / 2 d / 7 d, or permanent (default) |
| Banned extensions | Executables, scripts, potentially dangerous files |
| Upload rate | 60 req/hour/IP (anti-abuse) |
| View rate | 25 req/min/IP → then 5,000 req/hour/IP |

Complete limits table → **[docs/limits.md](docs/limits.md)**

---

## Security & Privacy

- **HTTPS everywhere**, HSTS, strict CSP on every page
- **Zero third-party scripts** — no analytics, no trackers, no pixels
- **Uploader IP** retained only for anti-abuse (malware/DMCA reports)
- **Malware scan** on every upload
- **Expired files** return `410 Gone` and are purged
- **Delete anonymous files** with the `userhash` returned at upload time

Security policy → **[SECURITY.md](SECURITY.md)**

---

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">
  <sub>Built by <a href="https://github.com/BhagattJii">bhagat jii</a> · <a href="https://meowbox.dpdns.org">meowbox.dpdns.org</a></sub>
</div>