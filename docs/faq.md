# MeowBox FAQ — 20+ Questions Answered

---

## Getting Started

### 1. What is MeowBox?
MeowBox is a free file hosting service that gives you a **direct link** for every upload. No ads, no trackers, no required accounts, no paywalls. Upload → get link → share anywhere.

### 2. How much does it cost?
**Zero.** No subscriptions, no premium tiers, no hidden fees. The service is funded privately and runs on Cloudflare's free tier.

### 3. Do I need an account?
**No.** Anonymous uploads work out of the box. A free account only adds a dashboard, albums, and the ability to delete your files later.

### 4. What file types are allowed?
Images (JPG, PNG, WebP, BMP, sanitized SVG), video (MP4, WebM), audio (MP3, OGG, WAV), PDF, text, archives (ZIP), fonts — essentially anything except executables and scripts. Max 25 MB per file (GIFs 20 MB).

### 5. What is banned?
Executables (`.exe`, `.jar`, `.scr`, `.cpl`, `.msi`, `.bat`, `.cmd`, `.vbs`, `.ps1`, `.apk`, `.php`, `.htaccess`, etc.), malware, and illegal content. Full list in [docs/LIMITS.md](limits.md).

---

## Uploads & Links

### 6. How long do links last?
**Permanent by default.** You can also choose an expiry at upload: 2 hours, 24 hours, 2 days, or 7 days. Expired links return `410 Gone` and the file is purged.

**View limits.** Also at upload you can pick how many times the link may be opened: **1 view** (a one-shot link), **2 views**, or unlimited (default). After the last allowed view the link returns `410 Gone - view limit reached` and the file is purged from storage. Preview bots (Discord, Telegram, ...) and HEAD requests do not consume views.

### 7. Can I delete an anonymous upload?
Only if you saved the **userhash** returned at upload time (`Registered! Your userhash: ...`). Without it, anonymous files cannot be deleted via API. (Account uploads are deletable from the dashboard.)

### 8. What is the maximum file size?
**25 MB** per file. **GIFs are capped at 20 MB** — convert to WebM for larger animations.

### 9. Can I upload from a URL instead of my computer?
Yes — use `reqtype=urlupload` with the `url` field. The remote file is fetched (max 25 MB), scanned, and hosted just like a direct upload.

### 10. Are there upload rate limits?
**60 uploads per hour per IP.** Exceeding returns `429`. See [docs/LIMITS.md](limits.md) for all rate limits.

---

## Accounts & Dashboard

### 11. How do I create an account?
Click **Register** on the site. Username: 3–32 chars (`a-z`, `0-9`, `_`), password: min 8 chars, email optional. You get a `userhash` (keep it secret) and a 30-day session cookie.

### 12. What does an account give me?
- Dashboard at `/manage` (list your files, hits, expiries)
- Create/edit/delete albums
- Delete files without needing the upload `userhash`
- API access with your `userhash`

### 13. Can I change my password / email?
Not currently supported in the UI. Delete the account and re-register if needed.

### 14. How do I delete my account?
Not implemented yet. Contact `meowboxteam@gmail.com` for manual removal.

---

## API Usage

### 15. What is the API endpoint?
`POST https://meowbox.dpdns.org/user/api.php` — one endpoint, `reqtype` tells it what to do.

### 16. How do I authenticate API calls?
Either:
- **Session cookie** (from web login) — browser only
- **`userhash` form field** — returned at registration or first upload

### 17. Can I use the API from a script / bot?
Yes. Example in [docs/API.md](api.md). Include a descriptive `User-Agent` (e.g., `MyBot/1.0`).

### 17. What `reqtype` values exist?
| `reqtype` | Action |
|-----------|--------|
| `fileupload` | Upload a local file |
| `urlupload` | Fetch & host a remote URL |
| `deletefiles` | Delete your files (needs `userhash`) |
| `createalbum` | Create an album |
| `editalbum` | Edit album title/desc & file list |
| `addtoalbum` | Add files to album |
| `removefromalbum` | Remove files from album |
| `deletealbum` | Delete album (files stay) |

Full details & curl examples → **[docs/API.md](api.md)**

---

## Security & Privacy

### 18. Is there malware scanning?
**Yes.** Every upload is hashed (SHA-256) and checked against MalwareBazaar (abuse.ch) and optionally VirusTotal. Known malware is blocked and permanently blacklisted. Scan failures fail open (file accepted) to avoid availability loss.

### 19. Do you track me?
**No.** No analytics, no third-party scripts, no pixels, no cookies except the session cookie for logged-in users. IP is retained only for anti-abuse (malware/DMCA reports).

### 20. What happens to my IP?
Logged at upload for 30 days (rate limiting, abuse reports). Not sold, not shared, not used for marketing.

### 21. Can I report abuse / DMCA?
Yes. Email `meowboxteam@gmail.com` with the direct link (`/f/xxxxxx`) and details. We act on valid reports promptly.

### 22. Are files encrypted at rest?
Files in KV are stored as-is (Cloudflare encrypts at rest). Files in the remote object store are stored per that provider's encryption. No client-side encryption — if you need it, encrypt before upload.

---

## Technical

### 23. Why does my GIF look bad / get rejected?
GIFs > 20 MB are rejected. Convert to **WebM** (VP9) or **MP4** (H.264) — smaller, smoother, better quality.

### 23. Why did I get `410 Gone`?
The link expired (you chose a TTL) or the file was deleted. Expired files are purged automatically.

### 24. Why `403` on upload?
- Banned extension / executable magic bytes
- Malware signature match
- Rate limit exceeded
- Invalid `userhash`

### 25. Why `429`?
Rate limit exceeded. See [docs/LIMITS.md](limits.md) for all buckets.

### 26. Does MeowBox support WebDAV / S3 API / FTP?
**No.** Only the HTTP API at `/user/api.php`.

### 27. Can I use a custom domain?
The service runs on `meowbox.dpdns.org`. Custom domains are not supported at this time.

### 28. Is there an SLA / uptime guarantee?
**No.** This is a free, best-effort service. No warranty, no SLA.

---

## Still Have Questions?

- Check the [Tools page](https://meowbox.dpdns.org/tools) for live limits & API examples
- Read the full docs in this repo: [HOW-IT-WORKS](how-it-works.md) • [API](api.md) • [LIMITS](limits.md) • [ARCHITECTURE](architecture.md)
- Email: `meowboxteam@gmail.com`
- GitHub Issues: [report a problem](https://github.com/BhagattJii/meowbox/issues) (no secrets!)
- Security issues: [GitHub Security Advisories](https://github.com/BhagattJii/meowbox/security/advisories/new)