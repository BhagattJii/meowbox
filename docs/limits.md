# MeowBox Limits — Complete Reference

Every limit is intentional, published, and enforced at the edge.

---

## File Limits

| Limit | Value | Notes |
|-------|-------|-------|
| **Max file size** | 25 MB | Hard limit, returns `413` |
| **GIF size** | 20 MB | Use WebM/MP4 for larger animations |
| **Expiry options** | 2 h, 24 h, 2 d, 7 d, or permanent (default) | `ttl` in seconds: `7200`, `86400`, `172800`, `604800`, `0` |
| **Banned extensions** | See table below | Blocked at upload, `403` |
| **Magic bytes blocked** | MZ (PE/EXE), ELF | Checked before storage, `403` |

### Banned Extensions (Case-Insensitive)

```
exe, scr, cpl, jar, msi, msix, bat, cmd, vbs, vbe,
wsf, wsh, ps1, psm1, hta, lnk, reg, apk, appx, xll,
doc, docm, docx, dot, dotx, htaccess, php, phtml
```

---

## Rate Limits (Enforced at Cloudflare Edge)

| Bucket | Limit | Window | Key | Response |
|--------|-------|--------|-----|----------|
| **Upload** (`fileupload`/`urlupload`) | 60 req | 1 hour | Client IP | `429` |
| **Signup** | 5 req | 1 hour | Client IP | `429` |
| **Login (per IP)** | 20 req | 15 min | Client IP | `429` |
| **Login (per username)** | 8 req | 15 min | IP + username | `429` |
| **View (soft)** | 25 req | 1 min | Client IP | soft throttle |
| **View (hard)** | 5,000 req | 1 hour | Client IP (after soft exceeded) | `429` |
| **API general** | 60 req | 1 hour | Client IP | `429` |

Exceeding returns `429` with plain-text error message.

---

## Account Limits

| Limit | Value | Notes |
|-------|-------|-------|
| **Username length** | 3–32 chars | `a-z`, `0-9`, `_` only |
| **Password min length** | 8 chars | No max enforced |
| **Email** | Optional, RFC 5322-ish | Not verified |
| **One account per person** | Soft policy | Not technically enforced |
| **Session TTL** | 30 days | HttpOnly, Secure, SameSite=Lax cookie |
| **Albums per user** | No hard limit | Reasonable use expected |
| **Files per album** | 500 max per operation | API enforces per-request cap |

---

## Storage & Expiry Behavior

| Scenario | Behavior |
|----------|----------|
| **Permanent link (default)** | File kept until explicit delete or account deletion |
| **Expiry chosen** | Auto-deleted at `expires_at`; returns `410 Gone` on access |
| **Expired file access** | Triggers immediate purge from storage + DB + cache; returns `410 Gone` |
| **Cron cleanup** | Runs every 15 min, processes up to 20 expired files per run |
| **KV soft cap** | 950 MB total; if exceeded, new uploads route to remote store |
| **Remote store capacity** | If unavailable → `503` for uploads that would use it |

---

## Album Limits

| Limit | Value |
|--------|-------|
| Files per album (per API call) | 500 |
| Album title/description | No enforced length (reasonable) |
| Albums per user | No hard limit |

---

## URL Upload Limits

| Limit | Value |
|-------|-------|
| Max download size | 25 MB |
| Timeout | 10 seconds (fetch) |
| Redirects | Followed (max 10) |
| Same validation as `fileupload` | Extensions, magic bytes, malware scan |

---

## Malware Scan Limits

| Aspect | Limit |
|--------|-------|
| Cache TTL | 30 days (KV) |
| VirusTotal threshold | `malicious + suspicious ≥ 3` |
| Fail-open | Any scan error → file accepted |
| Blocked hash retention | Permanent in `blocked_hashes` table |

---

## Cache & Headers on Served Files

| Header | Value |
|--------|-------|
| `cache-control` (KV) | `public, max-age=120, s-maxage=<min(600, ttl_left)>` |
| `cache-control` (remote) | `no-cache` (streamed) |
| `x-content-type-options` | `nosniff` |
| `access-control-allow-origin` | `*` |
| `cross-origin-resource-policy` | `cross-origin` |
| `strict-transport-security` | `max-age=31536000` |
| `referrer-policy` | `no-referrer` |

---

## Error Response Summary

| HTTP | Message | Cause |
|------|---------|-------|
| 400 | `Error: no file` / `invalid url` / `invalid reqtype` | Bad request |
| 401 | `Error: not logged in` | `/api/me` without session |
| 403 | `Error: invalid userhash` / `rate limited` / `file blocked` | Auth/quota/block |
| 404 | `404 Not Found` | File/album not found |
| 405 | `Error: use POST` | Wrong method on API |
| 410 | `410 Gone - link expiry time reached` | Expired link |
| 413 | `Error: file too large (max 25MB)` | Size limit |
| 429 | `Error: slow down` / `too many attempts` | Rate limit |
| 500 | `Error: uploads disabled` | Storage backend down |
| 503 | `Error: service temporarily at capacity` | KV soft cap hit |

All errors: `text/plain; charset=utf-8`, no JSON.

---

## What Happens at Each Limit

| Limit Hit | User Experience |
|-----------|-----------------|
| File > 25 MB | `413` immediately, no upload |
| GIF > 20 MB | `403` with "gif too large, use webm" |
| Banned extension | `403` "file extension not allowed" |
| Executable magic bytes | `403` "executable files not allowed" |
| Upload rate > 60/hr | `429` "slow down" |
| View rate > 25/min | Soft throttle, then `429` after 5,000/hr |
| Signup > 5/hr/IP | `429` "too many signups from this device" |
| Login > 20/15min/IP | `429` "too many login attempts, try again in 15 min" |
| Login > 8/15min/user | `429` "too many attempts, wait 15 min" |
| KV soft cap (950 MB) | New large/permanent uploads → remote store; if remote fails → `503` |
| Malware hash match | `403` "file blocked (malware detected)" |

---

## Limits by Design

- **No hidden quotas** — every cap is documented here and on the [Tools page](https://meowbox.dpdns.org/tools).  
- **No paid tiers** — all features free, no VIP, no premium.  
- **No password-protected links** — expiry and deletion are the access controls.  
- **No single-file uploads above 25 MB** — split or use WebM for video.  
- **No album viewer page** — albums managed via API only.