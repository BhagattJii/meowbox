# MeowBox Architecture

High-level system design, data flow, and technology choices — no implementation code.

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Edge compute** | Cloudflare Workers (JavaScript, V8 isolates) | Request handling, routing, auth, rate limiting, HTML serving |
| **Metadata DB** | Cloudflare D1 (SQLite) | File metadata, users, sessions, albums, rate counters, blocked hashes |
| **Primary blob storage** | Cloudflare KV (edge key-value) | Expiring files and files above 20 MB (≤ 25 MB) |
| **Secondary blob storage** | Telegram private channel via Bot API | Permanent files ≤ 20 MB and overflow when KV is near its soft cap |
| **Malware scan cache** | Cloudflare KV | 30-day cache of SHA-256 → `ok`/`bad` |
| **Cron** | Cloudflare Workers Cron Triggers (`*/15 * * * *`) | Purge expired files, clean sessions, maintenance |
| **Assets** | Inline static assets bundled into the Worker module | HTML/CSS/JS/images served with caching headers |
| **External APIs** | AlienVault OTX (default), MalwareBazaar / VirusTotal (optional) | Hash reputation lookup |
| **DNS / CDN** | Cloudflare (custom domain `meowbox.dpdns.org`) | TLS, HSTS, caching, DDoS protection |

---

## Request Flow (Text Diagram)

```
┌─────────────┐
│   Client    │  (browser, curl, bot)
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────────────────────────┐
│ Cloudflare Edge (Worker)            │
│  ├─ Host redirect (.workers.dev → apex) │
│  ├─ Rate limit checks (KV counters) │
│  ├─ Router:                          │
│  │   ├─ /f/<short>        → serveFile      │
│  │   ├─ /user/api.php     → api()          │
│  │   ├─ /user/manage.php  → managePage     │
│  │   ├─ /api/me           → apiMe()        │
│  │   └─ /* (HTML)         → assets()       │
│  └─ Hash reputation check (fail-open)│
└─────────────────────────────────────┘
       │
       ├───────────────┬───────────────┐
       ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  D1 (SQL)   │  │   KV (edge) │  │ Remote Store│
│  metadata   │  │  blobs ≤25MB│  │ large/perm  │
└─────────────┘  └─────────────┘  └─────────────┘
```

---

## Data Model (D1 Tables)

| Table | Key Columns | Purpose |
|-------|-------------|---------|
| `files` | `short` (PK), `ext`, `size`, `sha256`, `mime`, `owner` (userhash), `ip`, `store` (`kv`/`tg`), `kv_key` or `tg_chat`/`tg_msg`/`tg_file_id`, `created`, `expires_at` (0=permanent), `view_limit`, `views` | Core file metadata |
| `users` | `id` (PK), `username`, `email`, `pass_hash` (salt:hash), `userhash` (24-char), `ip`, `created` | Accounts |
| `sessions` | `sid` (PK), `user_id`, `expires` | Login sessions (30-day TTL) |
| `albums` | `short` (PK), `title`, `descr`, `owner` (userhash), `created` | User albums |
| `album_files` | `album_short`, `file_short` (composite PK) | Many-to-many |
| `rate2` | `ip`, `w` (window), `n` | Hourly rate counters |
| `blocked_hashes` | `sha256` (PK), `note` | Malware blacklist |
| `blocked_md5` | `md5` (PK) | Legacy MD5 blocklist |
| `crawl_log` | `ts`, `ua`, `path` | Bot crawl tracking |

---

## Storage Tier Logic

| Condition | Tier | Reason |
|-----------|------|--------|
| Expiring file ≤ 25 MB, or any file ≤ 25 MB when Telegram is not configured | **KV (edge)** | Fast edge serving and automatic TTL |
| File > 20 MB (hard limit is 25 MB) | **KV (edge)** | Telegram's `getFile` download limit is 20 MB |
| Permanent file ≤ 20 MB with `BOT_TOKEN` configured | **Telegram channel** | Keeps permanent files off the KV free-tier quota |
| KV put fails, or KV soft cap reached and file ≤ 20 MB | **Telegram channel** | Overflow path |
| KV soft cap reached and file > 20 MB | **`503`** | The file cannot be served from Telegram at that size |

- **KV key**: 16-char hex, value = file blob, optional `expirationTtl` for expiring files.
- **Telegram ref**: channel message (`tg_chat`, `tg_msg`, `tg_file_id`) in a private channel.
- **Failover**: KV put failure → Telegram. Telegram failure or unavailable bot → `503`, and D1 metadata is kept.

---

## Malware Scanning Pipeline

```
Upload → SHA-256 (+ MD5 local blocklist)
    ├─ local blocklist hit → 403
    └─ KV cache mb:<sha256>?
         ├─ hit "ok"  → accept
         ├─ hit "bad" → 403
         └─ miss → MalwareBazaar (if MB_AUTHKEY)
                   → VirusTotal (if VT_API_KEY)
                   → AlienVault OTX (default)
              ├─ any match → KV put "bad" (30d), insert blocked_hashes, 403
              ├─ any error → fail-open (accept)
              └─ clean → KV put "ok" (30d), accept
```

- **Cache TTL**: 30 days (`expirationTtl: 2592000`).
- **Fail-open** ensures availability even if reputation services are down.
- **Coverage**: known-bad hashes only. This is not a full antivirus scan, so unknown malware can still pass.

---

## Expiry & Cleanup (Cron)

**Schedule**: `*/15 * * * *` (every 15 minutes)

1. Delete expired sessions (`sessions.expires < now`).
2. Select up to 20 expired files (`files.expires_at > 0 AND expires_at < now`).
3. For each:
   - Delete from KV (`kv_key`) or the Telegram channel (`deleteMessage`).
   - Delete from `files` table.
   - Delete related `album_files` rows.
   - Purge Cloudflare cache for `https://meowbox.dpdns.org/f/<short>` and workers.dev variants.
4. Commit all.

---

## Rate Limiting Implementation

- **Counters in D1** (`rate2` table): `(ip, window, count)`.
- **Upload quota**: 30 uploads/hour + 300 MB/day per IP, aggregated from the `files` table.
- **API general**: 60 requests/minute/IP.
- **Window**: 1 hour for uploads and signup, 15 min for login, 1 min → 1 hour for views.
- **Flood guard** (in-memory `viewHits` map): 25 req/min/IP soft, then 5,000/hr hard.
- **Signup**: 5/hr/IP (`rateCheck("R:" + ip, 5, 3600)`).
- **Login**: 20/15min/IP + 8/15min per username.

All limits return `429` with plain-text error.

---

## Authentication & Sessions

- **Session cookie**: `sess=<24-char>; HttpOnly; Secure; SameSite=Lax; Max-Age=2592000; Path=/`
- **Session TTL**: 30 days (`expires` in `sessions` table).
- **Password hashing**: PBKDF2-SHA256, 100k iterations, 16-byte salt, stored as `salt:hash`.
- **Userhash**: 24-char random hex, used for API auth (independent of session).
- **Anonymous uploads**: the client may supply a 24-char hex `userhash`; it becomes the file owner. The web uploader generates one and stores it in the browser. Without one, `owner = NULL` and the file cannot be deleted via the API.

---

## Security Boundaries

| Boundary | Protection |
|----------|------------|
| **Upload validation** | Extension allowlist, magic-byte block (MZ/ELF), size clamp, filename sanitization |
| **Malware checks** | SHA-256/MD5 blocklists + OTX reputation, optional MalwareBazaar/VirusTotal, 30d KV cache, fail-open |
| **Direct link access** | No auth required (by design), `410` on expiry, cache-controlled |
| **API auth** | Session cookie OR `userhash` form field; `userhash` validated against `users` table |
| **Delete authorization** | `owner == userhash` enforced per file; album ownership checked per album |
| **Rate limits** | Edge-enforced via D1 counters + in-memory flood guard |
| **CORS** | `access-control-allow-origin: *` on API and served files |
| **Headers** | `nosniff`, `cross-origin-resource-policy: cross-origin`, HSTS 1yr, `referrer-policy: no-referrer`, `content-disposition` |
| **CSP on HTML** | `default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; font-src 'self'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'; object-src 'none'` |

---

## SEO & Bot Behavior

- **Redirect**: `*.workers.dev` and `www.meowbox.dpdns.org` → `https://meowbox.dpdns.org` (301 + `X-Robots-Tag: noindex, nofollow`).
- **Sitemap**: `/sitemap.xml` covers all public pages, with `lastmod` updated on deploy.
- **IndexNow**: Key hosted at `/299acade1dc86348fa74d883ef20b3bd.txt`, all URLs submitted on deploy.
- **JSON-LD**: `Organization`, `WebSite`, `WebApplication`, `SoftwareApplication`, `HowTo`, `FAQPage`, `BreadcrumbList` on relevant pages.
- **Crawl logging**: Bots (`Googlebot`, `bingbot`, etc.) logged to D1 `crawl_log` table.
- **`robots.txt`**: Allows all, points to sitemap.
- **`security.txt`**: `/.well-known/security.txt` with contact + policy link.
- **Browserconfig**: `/browserconfig.xml` for Windows tile.

---

## Deployment Topology

```
GitHub (docs repo)          Cloudflare (runtime)
     │                            │
     │  (manual deploy)           │
     ▼                            ▼
scripts/deploy.py (local) ──→  Worker "www"
                                 │
                                 ├─ D1 database "meowbox-db"
                                 ├─ KV namespace "KV"
                                 ├─ Inline static assets in worker.js
                                 ├─ Secrets: BOT_TOKEN, MB_AUTHKEY, VT_API_KEY
                                 └─ Cron: */15 * * * *
```

- **Deploy script**: `scripts/deploy.py` (reads secrets from env, bundles assets inline, uploads via CF API).
- **Wrangler config**: `wrangler.toml` defines bindings; `account_id` set via `CLOUDFLARE_ACCOUNT_ID` env.
- **Secrets**: `BOT_TOKEN` (Telegram), `MB_AUTHKEY` (MalwareBazaar), `VT_API_KEY` (VirusTotal) — stored as Worker secrets, never in repo.
- **No CI/CD pipeline** in this repo (secrets not in GitHub); deploy is a manual local step.

---

## Observability

- **Crawl log** (D1): timestamp, user-agent (truncated), path — for SEO monitoring.
- **Rate counters** (D1 `rate2`): per-window counts for debugging.
- **Worker logs**: available in Cloudflare dashboard (tail, exceptions).
- **No external APM** — keeping stack minimal and private.

---

## Scaling Considerations

| Dimension | Current Headroom | Mitigation |
|-----------|------------------|------------|
| KV storage | 950 MB soft cap (well below) | Remote store overflow |
| D1 rows | SQLite, ~millions OK | Partition by date if needed |
| KV ops | Free-tier daily quotas apply | Edge cache reduces reads |
| Cron batch | 20 files/run | Increase limit if backlog |
| Malware lookup latency | Sequential providers, 6–10s timeouts | Fail-open, 30d cache |

---

## What This Repo Does NOT Contain

- Worker source (`src/worker.js`)
- Build/deploy scripts with secrets
- Database dumps or user data
- Operational credentials

This is a **documentation-only** repository. The service source is deployed from a separate, private working directory.