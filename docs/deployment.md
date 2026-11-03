# Deploying Your Own MeowBox Instance

This guide explains how to deploy a MeowBox-compatible file host on Cloudflare Workers using the same architecture.

> **Note**: This repository contains **documentation only**. The service source code is not published here. This guide describes the required bindings, secrets, and configuration — you will need to write your own Worker or adapt a compatible open-source alternative.

---

## Prerequisites

- Cloudflare account with Workers Paid plan (for D1, KV, Cron Triggers)
- `wrangler` CLI installed (`npm install -g wrangler` or `pipx install wrangler`)
- Git (for version control)
- Node.js ≥ 18 (for local dev/testing)

---

## 1. Create Cloudflare Resources

### D1 Database
```bash
wrangler d1 create meowbox-db
# Note the database_id from output
```

Run the schema (see `schema.sql` in this repo):
```bash
wrangler d1 execute meowbox-db --file=schema.sql
```

### KV Namespace
```bash
wrangler kv:namespace create "KV"
# Note the id from output (for production)
wrangler kv:namespace create "KV" --preview
# Note the preview_id (for local dev)
```

### Worker Script
```bash
wrangler deploy --name meowbox --dry-run
# Creates the script placeholder
```

---

## 2. Configure `wrangler.toml`

Create `wrangler.toml` in your project root (use placeholders, fill in your IDs):

```toml
name = "meowbox"
main = "src/worker.js"
compatibility_date = "2026-01-01"

# Set via env var: CLOUDFLARE_ACCOUNT_ID
# account_id = "YOUR_ACCOUNT_ID"

[assets]
directory = "./public"
binding = "ASSETS"
run_worker_first = true

[[d1_databases]]
binding = "DB"
database_name = "meowbox-db"
database_id = "YOUR_D1_DATABASE_ID"   # from step 1

[[kv_namespaces]]
binding = "KV"
id = "YOUR_KV_ID"                     # production
preview_id = "YOUR_KV_PREVIEW_ID"     # local dev

[vars]
SITE_NAME = "MeowBox"
CHANNEL_USERNAME = "your_telegram_channel"   # without @
MAX_SIZE_MB = "25"
KV_MAX_MB = "25"
```

---

## 3. Set Secrets (Never in Repo)

```bash
# Telegram bot token (for remote storage tier)
wrangler secret put BOT_TOKEN
# → paste your bot token (format: 123456:ABC-DEF...)

# MalwareBazaar auth key (optional, for malware scanning)
wrangler secret put MB_AUTHKEY
# → paste your abuse.ch API key

# VirusTotal API key (optional, secondary scanner)
wrangler secret put VT_API_KEY
# → paste your VirusTotal v3 key
```

---

## 4. Project Structure

```
my-meowbox/
├── src/
│   └── worker.js          # Your Worker implementation
├── public/                # Static assets (served via ASSETS binding)
│   ├── index.html
│   ├── style.css
│   ├── upload.js
│   ├── favicon.ico
│   ├── logo.png
│   ├── banner.webp
│   ├── robots.txt
│   ├── sitemap.xml
│   ├── browserconfig.xml
│   ├── .well-known/security.txt
│   └── ... (other pages)
├── schema.sql             # D1 schema (from this repo)
├── wrangler.toml          # Config (with your IDs)
├── package.json           # Optional: for lint/test scripts
└── README.md
```

---

## 5. Local Development

```bash
# Start local dev server (uses preview KV, local D1)
wrangler dev

# Test upload
curl -X POST http://localhost:8787/user/api.php \
  -F "reqtype=fileupload" \
  -F "fileToUpload=@test.jpg"
```

---

## 6. Deploy to Production

```bash
# Deploy Worker + assets
wrangler deploy

# Deploy cron trigger (every 15 min)
wrangler deploy --cron "*/15 * * * *"
# Or add to wrangler.toml:
# [triggers]
# crons = ["*/15 * * * *"]
```

---

## 7. Post-Deploy Verification

```bash
# 1. Homepage loads
curl -I https://your-subdomain.workers.dev/

# 2. Upload test
curl -X POST https://your-subdomain.workers.dev/user/api.php \
  -F "reqtype=fileupload" -F "fileToUpload=@test.jpg"
# → should return direct link

# 3. Serve test
curl -I https://your-subdomain.workers.dev/f/<short>

# 4. Sitemap
curl https://your-subdomain.workers.dev/sitemap.xml

# 5. SEO files
curl -I https://your-subdomain.workers.dev/robots.txt
curl -I https://your-subdomain.workers.dev/browserconfig.xml
curl -I https://your-subdomain.workers.dev/.well-known/security.txt
```

---

## 8. Custom Domain (Optional)

```bash
# Add custom domain in Cloudflare Dashboard → Workers → Triggers → Custom Domains
# Or via CLI:
wrangler custom-domain add meowbox.example.com --zone example.com
```

Then update `SITE_NAME` and canonical URLs in your HTML/JSON-LD.

---

## 9. SEO & IndexNow (Automate)

Create a deploy script that:
1. Runs `wrangler deploy`
2. Submits sitemap URLs to IndexNow:

```python
import json, urllib.request, xml.etree.ElementTree as ET

KEY = "your-indexnow-key"
URLS = [e.text for e in ET.parse("public/sitemap.xml").getroot().iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]

body = {"host": "your-domain.com", "key": KEY, "keyLocation": f"https://your-domain.com/{KEY}.txt", "urlList": URLS}
req = urllib.request.Request("https://api.indexnow.org/indexnow", json.dumps(body).encode(), {"Content-Type": "application/json"})
print(urllib.request.urlopen(req).status)  # 200 = success
```

---

## 10. Monitoring & Maintenance

| Task | Frequency | Command |
|------|-----------|---------|
| Check Worker logs | Daily | `wrangler tail` |
| Monitor D1 size | Weekly | `wrangler d1 execute meowbox-db --command "SELECT COUNT(*) FROM files"` |
| KV usage | Weekly | Cloudflare Dashboard → Workers KV |
| Cron health | Daily | Check `cron` logs in Dashboard |
| Malware scan cache hit rate | Monthly | Query KV `mb:*` keys |
| IndexNow submission | Every deploy | Verify 200 response |

---

## 11. Schema Reference

The `schema.sql` in this repo creates:

```sql
CREATE TABLE files (
  short TEXT PRIMARY KEY,
  ext TEXT, size INTEGER, sha256 TEXT, mime TEXT,
  owner TEXT, ip TEXT, store TEXT,      -- 'kv' or 'remote'
  kv_key TEXT, remote_ref TEXT,
  created REAL, expires_at REAL         -- 0 = permanent
);
CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, email TEXT, pass_hash TEXT, userhash TEXT UNIQUE, ip TEXT, created REAL);
CREATE TABLE sessions (sid TEXT PRIMARY KEY, user_id INTEGER, expires REAL);
CREATE TABLE albums (short TEXT PRIMARY KEY, title TEXT, descr TEXT, owner TEXT, created REAL);
CREATE TABLE album_files (album_short TEXT, file_short TEXT, PRIMARY KEY (album_short, file_short));
CREATE TABLE rate2 (ip TEXT, w INTEGER, n INTEGER, PRIMARY KEY (ip, w));
CREATE TABLE blocked_hashes (sha256 TEXT PRIMARY KEY, note TEXT);
CREATE TABLE blocked_md5 (md5 TEXT PRIMARY KEY);
CREATE TABLE crawl_log (ts INTEGER, ua TEXT, path TEXT);
CREATE INDEX idx_files_owner ON files(owner);
CREATE INDEX idx_files_expires ON files(expires_at);
```

---

## 12. Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| `403` on upload | Banned extension / magic bytes / malware | Check `BANNED_EXT` list, file type |
| `503` capacity | KV soft cap (950 MB) + remote store down | Check remote store credentials, KV usage |
| `410` immediately | TTL set to 0 but `expires_at` wrong | Ensure `ttl=0` → `expires_at=0` in DB |
| `404` on serve | KV key deleted / remote message gone | Check cron logs, remote store retention |
| Cron not running | Trigger not deployed | `wrangler deploy --cron "*/15 * * * *"` |
| IndexNow 400 | Key mismatch / wrong host | Verify key file at `/.well-known/` matches |

---

## 13. Security Checklist

- [ ] All secrets in `wrangler secret`, never in repo
- [ ] `account_id` via `CLOUDFLARE_ACCOUNT_ID` env var
- [ ] `BOT_TOKEN` has minimal permissions (sendDocument, getFile, deleteMessage)
- [ ] `MB_AUTHKEY` / `VT_API_KEY` restricted to your IP if possible
- [ ] CSP headers on all HTML responses
- [ ] HSTS 1 year, `nosniff`, `cross-origin-resource-policy: cross-origin`
- [ ] Rate limits enforced on all mutating endpoints
- [ ] Malware scan fail-open (availability over strictness)
- [ ] No secrets in logs (Worker tail redacted)

---

## 14. Support

- **Docs**: this repo (`docs/`)
- **Issues**: [GitHub Issues](https://github.com/BhagattJii/meowbox/issues)
- **Security**: [Security Advisories](https://github.com/BhagattJii/meowbox/security/advisories/new)
- **Email**: `meowboxteam@gmail.com`

---

*This deployment guide is provided as-is. The MeowBox service at `meowbox.dpdns.org` is operated by BhagattJii and is not affiliated with Cloudflare, Telegram, MalwareBazaar, or VirusTotal.*