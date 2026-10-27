<div align="center">

# MeowBox

**Free, no-ads file hosting with direct links.**

Drop a file, get a link, share it anywhere. No ads, no trackers, no paywall.

[![Website](https://img.shields.io/badge/website-meowbox.dpdns.org-4c9aff?style=flat-square&logo=cloudflare)](https://meowbox.dpdns.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![API](https://img.shields.io/badge/API-REST-informational?style=flat-square)](https://meowbox.dpdns.org/tools)

[Website](https://meowbox.dpdns.org) · [FAQ](https://meowbox.dpdns.org/faq) · [Tools & API](https://meowbox.dpdns.org/tools) · [Safety](https://meowbox.dpdns.org/safety) · [Legal](https://meowbox.dpdns.org/legal)

</div>

---

## Features

- **Direct links** — every upload gets a hotlinkable URL (`/f/xxxxxx`) that works in Discord, forums, blogs and chats
- **Anonymous uploads** — no email, no signup, no login
- **Expiring links** — permanent by default, or auto-delete after 2 hours / 24 hours / 2 days / 7 days (returns `410 Gone`)
- **Albums & delete control** — a free account adds a dashboard, albums and one-click deletion
- **Malware scanning on every upload** — executables are banned outright, known-bad signatures are permanently blacklisted
- **All file types** — images (JPG, PNG, WebP, BMP, sanitized SVG), video, audio, PDF and archives up to 25 MB (GIFs capped at 20 MB)
- **REST API** — one `POST` endpoint, one `reqtype` field per action
- **No tracking** — no ads, no analytics, no tracking pixels, no data sold, no AI training on your files

## Limits

| Rule | Limit |
|---|---|
| Max file size | 25 MB (GIF: 20 MB) |
| Expiry options | 2 hours · 24 hours · 2 days · 7 days |
| Executables / scripts | Blocked |
| Account | Optional — only for dashboard, albums, deletes |

## API

Everything the web UI does is available over HTTP. Send a `POST` to `/user/api.php` with a `reqtype` field — one request per action.

| `reqtype` | Action |
|---|---|
| `fileupload` | Upload a file |
| `urlupload` | Fetch and host a remote URL |
| `deletefiles` | Delete files (anonymous uploads need the `userhash` returned at upload time) |
| `createalbum` | Create an album |
| `editalbum` | Edit an album |
| `addtoalbum` | Add files to an album |
| `removefromalbum` | Remove files from an album |
| `deletealbum` | Delete an album |

Request details and ready-to-run examples: **[meowbox.dpdns.org/tools](https://meowbox.dpdns.org/tools)**

## Security & privacy

- HTTPS enforced everywhere, 1-year HSTS, strict Content-Security-Policy on every page
- Zero third-party scripts, ads or trackers
- Uploader IP is retained only for anti-abuse (malware / DMCA reports) — see the [legal page](https://meowbox.dpdns.org/legal)
- Every upload is scanned before it is stored or served

## Contributing

Issues and pull requests are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

Built by [BhagattJii](https://github.com/BhagattJii).
