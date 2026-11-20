# How MeowBox Works

This document explains the request lifecycle, storage model, expiry and view-limit handling, malware scanning, and rate limits — in plain language, no implementation code.

---

## Request Lifecycle

1. **Client uploads**  
   - Browser POSTs multipart form to `/user/api.php` with `reqtype=fileupload` (or `urlupload`).  
   - Web UI on the homepage does the same via JavaScript.

2. **Worker validates**  
   - Checks rate limits (30 uploads/hour and 300 MB/day per IP).  
   - Verifies file size ≤ 25 MB (GIF ≤ 20 MB).  
   - Rejects banned extensions and magic bytes (MZ/ELF).

3. **Hash reputation check** (before storage)  
   - Computes SHA-256 and MD5 of the file.  
   - Checks local SHA-256/MD5 blocklists and the 30-day KV cache (`mb:<hash>` → `ok`/`bad`).  
   - If not cached, queries MalwareBazaar (when configured), VirusTotal (when configured), and AlienVault OTX (default).  
   - On a match → file blocked, hash cached, DB row inserted in `blocked_hashes`.  
   - Lookup failures (timeout, API down) **fail open** — file is accepted to preserve availability.  
   - This is not a full antivirus scan; unknown malware can pass.

4. **Storage decision**  
   - **Tier 1 (Edge KV)**: files ≤ 25 MB with short TTL (2 h / 24 h / 2 d / 7 d) or when KV usage is under soft cap (950 MB).  
   - **Tier 2 (Telegram private channel)**: permanent files up to 20 MB, or overflow when Tier 1 is at capacity.  
   - Files above 20 MB stay in KV because Telegram's download API caps at 20 MB; if KV is full, they return `503`.

5. **Metadata persisted** (D1)  
   - `files` table: `short` (12-char ID), `ext`, `size`, `sha256`, `mime`, `owner` (userhash or `NULL`), `ip`, `store` (`kv`/`tg`), `kv_key` or `tg_file_id`/`tg_msg`, `created`, `expires_at` (0 = permanent), `view_limit`, `views`.

6. **Response**  
   - Returns plain text direct link: `https://meowbox.dpdns.org/f/<short>`.

---

## Serving a File (`GET /f/<short>`)

1. **Rate check** — 25 views/min/IP, then 5,000/hr/IP (flood guard).  
2. **DB lookup** — if not found → `404`.  
3. **Expiry check** — if `expires_at > 0` and now > `expires_at`:  
   - Delete from KV / remote store.  
   - Remove DB row.  
   - Purge Cloudflare cache for the short ID.  
   - Return `410 Gone - link expiry time reached`.
   - View limits: if the file has a view limit and the request is a real open (GET, not a preview bot or HEAD), the view counter is incremented atomically. When the limit is exhausted the link returns `410 Gone - view limit reached` and the file is purged. Limited links are never cached (edge or browser), so only genuine opens are counted. A background sweep also purges exhausted limited files.
4. **Cache hit** — for KV-stored files, try Cloudflare cache first.  
5. **Serve**  
   - KV: read from KV, set `cache-control: public, max-age=120, s-maxage=<ttl>`.  
   - Remote: fetch from remote store, stream to client, cache URL in KV for 24 h.  
   - `content-type` by extension; HTML/HTM/PHP/SVG/JS are forced to `text/plain` and `attachment`.  
   - `content-disposition` uses the short ID (`<short>.<ext>`); HTTP Range requests are not supported.  
   - Security headers: `nosniff`, CORS `*`, `cross-origin-resource-policy: cross-origin`, HSTS, `referrer-policy: no-referrer`.

---

## Expiry & Cleanup

- **Cron** runs every 15 minutes (`*/15 * * * *`):  
  - Deletes expired sessions.  
  - Finds up to 20 expired files per run, deletes from KV/remote, removes DB rows, purges cache.  
- **On-demand**: serving an expired file triggers immediate purge and `410`.

---

## Malware Scanning Details

| Aspect | Behavior |
|--------|----------|
| Hash | SHA-256, plus an MD5 local blocklist |
| Primary source | AlienVault OTX public hash reputation, active by default |
| Optional sources | MalwareBazaar `get_info` (with `MB_AUTHKEY`) and VirusTotal v3 (with `VT_API_KEY`) |
| Cache | KV key `mb:<hash>` → `ok` or `bad`, TTL 30 days |
| Fail open | Any lookup error → file accepted, no block |
| Block threshold | VirusTotal: `malicious + suspicious ≥ 3` (when configured) |
| DB record | `blocked_hashes(sha256, note)` and legacy `blocked_md5` |
| Coverage | Known-bad hashes only; not a full antivirus scan, so unknown malware can pass |

---

## Rate Limits (Enforced at Edge)

| Bucket | Limit | Window | Key |
|--------|-------|--------|-----|
| Upload | 30 req | 1 hour | client IP |
| Upload data | 300 MB | 24 hours | client IP |
| Signup | 5 req | 1 hour | client IP |
| Login (IP) | 20 req | 15 min | client IP |
| Login (per user) | 8 req | 15 min | IP + username |
| View (soft) | 25 req | 1 min | client IP |
| View (hard) | 5,000 req | 1 hour | client IP (after soft exceeded) |
| API general | 60 req | 1 min | client IP |

Limits return `429` with plain-text error.

---

## Accounts & Authentication

- **Anonymous uploads**: no account needed. Send a 24-char hex `userhash` at upload to own the file; the web uploader generates and saves one. Without it, `owner = NULL` and the file cannot be deleted via the API.  
- **Registration**: username 3–32 chars (`a-z0-9_`), password ≥ 8 chars, optional email (validated).  
  - Password hashed with PBKDF2-SHA256 (100k iterations, 16-byte salt).  
  - `userhash` = 24-char random string (used for API auth).  
  - Session cookie `sess` (HttpOnly, Secure, SameSite=Lax, 30-day TTL).  
- **Login**: same rate limits, sets session cookie, redirects to `/manage`.  
- **API auth**: either session cookie or `userhash`/`key` form field.

---

## Albums

- Owned by a `userhash`.  
- CRUD via `reqtype`: `createalbum`, `editalbum`, `addtoalbum`, `removefromalbum`, `deletealbum`.  
- `files` array in form data links files to album.

---

## URL Upload (`reqtype=urlupload`)

- Fetches remote URL (max 25 MB), follows redirects, extracts filename/extension from final URL.  
- Same validation, scanning, storage as direct upload.

---

## Error Responses

All errors are plain text with HTTP status:

| Code | Typical cause |
|------|---------------|
| 400 | Bad request (missing file, invalid URL, bad extension) |
| 401 | Not logged in (session required) |
| 403 | Rate limited, banned hash, invalid userhash, not your file |
| 404 | File not found |
| 405 | Method not allowed |
| 410 | Link expired |
| 413 | File too large (> 25 MB) |
| 429 | Rate limit exceeded |
| 500 | Internal (e.g., uploads disabled or storage unavailable) |
| 503 | Service at capacity, or a Telegram-backed file while the bot is not configured |

---

## Security Headers on Served Files

```
content-type: <by extension, safe list forced to text/plain>
content-disposition: inline (attachment for HTML/HTM/PHP/SVG/JS)
cache-control: no-cache (KV: public, max-age=120, s-maxage=...)
x-content-type-options: nosniff
access-control-allow-origin: *
cross-origin-resource-policy: cross-origin
strict-transport-security: max-age=31536000
referrer-policy: no-referrer
```

---

## What Is NOT in This Repo

- The Worker source code (`src/worker.js`)  
- Build/deploy scripts with secrets  
- Database dumps, user files, or any operational data  

This repo is **documentation only**. The service runs on Cloudflare Workers + D1 + KV + a Telegram-backed private channel.