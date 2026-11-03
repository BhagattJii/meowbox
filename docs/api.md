# MeowBox API Reference

Base URL: `https://meowbox.dpdns.org`  
API endpoint: `POST /user/api.php`  
All responses are **plain text** (direct link, error message, or `userhash`).  
Authentication: session cookie (`sess`) **or** `userhash`/`key` form field.

---

## Common Fields

| Field | Required | Description |
|-------|----------|-------------|
| `reqtype` | Yes | Action to perform (see table below) |
| `userhash` / `key` | For authenticated actions | 24-char string returned at registration/upload |
| `ttl` | Optional | Link lifetime in seconds: `0` (default, permanent), `7200` (2 h), `86400` (24 h), `172800` (2 d), `604800` (7 d). Values outside range are clamped. |

---

## `reqtype` Values

| `reqtype` | Auth | Description |
|-----------|------|-------------|
| `fileupload` | Optional | Upload a file from local disk |
| `urlupload` | Optional | Fetch a remote URL and host it |
| `deletefiles` | **Required** | Delete one or more of your files |
| `createalbum` | **Required** | Create a new album |
| `editalbum` | **Required** | Edit album title/description & replace file list |
| `addtoalbum` | **Required** | Add files to an existing album |
| `removefromalbum` | **Required** | Remove files from an album |
| `deletealbum` | **Required** | Delete an album (files remain) |

---

## 1. `fileupload` — Upload a Local File

**Fields**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `fileToUpload` | file | Yes | The file to upload |
| `ttl` | integer | No | Link lifetime in seconds (0 = permanent) |

**Response**  
`200 OK` → direct link: `https://meowbox.dpdns.org/f/abc123xyz`  
`4xx/5xx` → error message (see [Error Codes](#error-codes))

**Example**
```bash
curl -X POST https://meowbox.dpdns.org/user/api.php \
  -F "reqtype=fileupload" \
  -F "fileToUpload=@photo.jpg" \
  -F "ttl=0"
# → https://meowbox.dpdns.org/f/abc123xyz
```

**With account (for dashboard/delete later)**
```bash
curl -X POST https://meowbox.dpdns.org/user/api.php \
  -F "reqtype=fileupload" \
  -F "fileToUpload=@photo.jpg" \
  -F "userhash=YOUR_USERHASH"
# → https://meowbox.dpdns.org/f/abc123xyz
```

---

## 2. `urlupload` — Fetch & Host a Remote URL

**Fields**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `url` | string | Yes | Public HTTP/HTTPS URL to fetch |
| `ttl` | integer | No | Link lifetime in seconds |
| `userhash` | string | No | Associate with your account |

**Behavior**  
- Follows redirects, max 25 MB download.  
- Filename/extension derived from final URL.  
- Same validation, scanning, storage as `fileupload`.

**Response**  
Direct link on success, error message on failure.

**Example**
```bash
curl -X POST https://meowbox.dpdns.org/user/api.php \
  -F "reqtype=urlupload" \
  -F "url=https://example.com/video.mp4" \
  -F "ttl=172800"
```

---

## 3. `deletefiles` — Delete Your Files

**Auth required** — `userhash` (or session cookie).

**Fields**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `files` / `files[]` | string (repeatable) | Yes | Short IDs to delete, up to 500 per request |

**Behavior**  
- Only deletes files where `owner == your userhash`.  
- Removes from KV / remote store, DB, album links, and Cloudflare cache.  
- Returns `Deleted N file(s)` or `Error: nothing deleted (not yours)`.

**Example**
```bash
curl -X POST https://meowbox.dpdns.org/user/api.php \
  -F "reqtype=deletefiles" \
  -F "userhash=YOUR_USERHASH" \
  -F "files=abc123xyz" \
  -F "files=def456uvw"
```

---

## 4. `createalbum` — Create an Album

**Auth required** — `userhash`.

**Fields**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `title` | string | No | Album title |
| `desc` | string | No | Album description |
| `files` | string | No | Space-separated short IDs to add initially |

**Response**  
Album short ID (12 chars) on success.

**Example**
```bash
curl -X POST https://meowbox.dpdns.org/user/api.php \
  -F "reqtype=createalbum" \
  -F "userhash=YOUR_USERHASH" \
  -F "title=Vacation 2026" \
  -F "desc=Photos from the trip" \
  -F "files=abc123xyz def456uvw"
```

---

## 5. `editalbum` — Edit Album Metadata & File List

**Auth required** — `userhash` (must own the album).

**Fields**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `short` | string | Yes | Album short ID |
| `title` | string | No | New title |
| `desc` | string | No | New description |
| `files` | string | No | Space-separated short IDs (replaces entire list) |

**Example**
```bash
curl -X POST https://meowbox.dpdns.org/user/api.php \
  -F "reqtype=editalbum" \
  -F "userhash=YOUR_USERHASH" \
  -F "short=alb123xyz" \
  -F "title=Updated title" \
  -F "files=abc123xyz newfile789"
```

---

## 6. `addtoalbum` — Add Files to Album

**Auth required** — `userhash` (must own the album).

**Fields**

| Field | Type | Required |
|-------|------|----------|
| `short` | string | Yes |
| `files` | string | Yes (space-separated) |

**Example**
```bash
curl -X POST https://meowbox.dpdns.org/user/api.php \
  -F "reqtype=addtoalbum" \
  -F "userhash=YOUR_USERHASH" \
  -F "short=alb123xyz" \
  -F "files=abc123xyz def456uvw"
```

---

## 7. `removefromalbum` — Remove Files from Album

**Auth required** — `userhash` (must own the album).

**Fields**

| Field | Type | Required |
|-------|------|----------|
| `short` | string | Yes |
| `files` | string | Yes (space-separated) |

---

## 8. `deletealbum` — Delete Album

**Auth required** — `userhash` (must own the album).

**Fields**

| Field | Type | Required |
|-------|------|----------|
| `short` | string | Yes |

**Behavior**  
Deletes album row and all `album_files` links. Files themselves are **not** deleted.

**Example**
```bash
curl -X POST https://meowbox.dpdns.org/user/api.php \
  -F "reqtype=deletealbum" \
  -F "userhash=YOUR_USERHASH" \
  -F "short=alb123xyz"
```

---

## Additional Endpoint: `/api/me`

**Method**: `GET`  
**Auth**: session cookie (logged in via web).  
**Response**: JSON with username, userhash, and your files (short, ext, size, created, hits, expires_at).

```bash
curl -H "Cookie: sess=YOUR_SESSION" https://meowbox.dpdns.org/api/me
# → {"username":"alice","userhash":"abc123...","files":[{"short":"xyz789","ext":"jpg",...}]}
```

---

## Error Codes

| HTTP | Message | Meaning |
|------|---------|---------|
| 400 | Error: no file / invalid url / invalid reqtype | Bad request |
| 401 | Error: not logged in | Session required for `/api/me` |
| 403 | Error: invalid userhash / rate limited / file blocked | Auth/quota/block |
| 404 | 404 Not Found | File/album not found |
| 405 | Error: use POST | Wrong method |
| 410 | 410 Gone - link expiry time reached | Expired file |
| 413 | Error: file too large (max 25MB) | Size limit |
| 429 | Error: slow down / too many attempts | Rate limit |
| 500 | Error: uploads disabled | Storage backend unavailable |
| 503 | Error: service temporarily at capacity | KV soft limit hit |

All errors return `text/plain` with the message.

---

## Rate Limits (Applied Per IP Unless Noted)

| Action | Limit | Window |
|--------|-------|--------|
| Upload (`fileupload`/`urlupload`) | 60 | 1 hour |
| Signup | 5 | 1 hour |
| Login (per IP) | 20 | 15 min |
| Login (per username) | 8 | 15 min |
| View (`GET /f/*`) | 25 → 5,000 | 1 min → 1 hour |
| API general | 60 | 1 hour |

Exceeding returns `429` with plain-text error.

---

## Complete Example: Upload → Delete

```bash
# 1. Register (once) → save userhash
curl -X POST https://meowbox.dpdns.org/user/register.php \
  -F "username=alice" -F "password=secret123" -F "email=alice@example.com"
# → Registered! Your userhash (keep it secret): abc123def456ghi789jkl012

# 2. Upload with userhash
curl -X POST https://meowbox.dpdns.org/user/api.php \
  -F "reqtype=fileupload" \
  -F "fileToUpload=@doc.pdf" \
  -F "userhash=abc123def456ghi789jkl012"
# → https://meowbox.dpdns.org/f/xyz789uvw

# 3. Later, delete it
curl -X POST https://meowbox.dpdns.org/user/api.php \
  -F "reqtype=deletefiles" \
  -F "userhash=abc123def456ghi789jkl012" \
  -F "files=xyz789uvw"
# → Deleted 1 file(s)
```

---

## Notes

- **Anonymous uploads** (no `userhash`) cannot be deleted via API — only by the `userhash` returned in the upload response text.  
- **Expired links** return `410 Gone` and are purged automatically.  
- **CORS**: all endpoints allow `*` origin.  
- **No JSON** — responses are plain text for simplicity.  
- **User agent**: include a descriptive UA (e.g., `MyApp/1.0`) to help debugging.