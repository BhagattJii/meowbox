# MeowBox Privacy Policy

**Effective**: 2026-10-30  
**Contact**: `meowboxteam@gmail.com` | [GitHub Security Advisories](https://github.com/BhagattJii/meowbox/security/advisories/new)

---

## What Data We Collect

| Data | Source | Retention | Purpose |
|------|--------|-----------|---------|
| **Uploader IP** | `cf-connecting-ip` header on every upload | Stored with file metadata until the file is deleted or expires; rate-limit counters are purged on a rolling schedule | Rate limiting, abuse/DMCA investigation |
| **File metadata** | Upload form (size, extension, MIME type, SHA-256) | Until file deleted or expires | Service operation, hash reputation checks, malware cache |
| **User account** | Registration form (username, email, password hash) | Until account deleted | Authentication, dashboard, album ownership |
| **Session cookie** | `sess` (HttpOnly, Secure, SameSite=Lax) | 30 days from last login | Keep user logged in |
| **Malware scan cache** | SHA-256 → `ok`/`bad` | 30 days in KV | Avoid repeat scans |
| **Crawl logs** | Bot user-agents (Googlebot, bingbot, etc.) | 90 days in D1 | SEO monitoring |

---

## What We Do NOT Collect

- No analytics, no tracking pixels, no third-party scripts
- No cookies except the session cookie for logged-in users
- No fingerprinting, no IndexedDB. localStorage is used only to remember your own upload links and anonymous delete key in this browser
- No advertising identifiers, no cross-site tracking
- No email verification, no marketing emails
- No AI training on uploaded files

---

## How We Use Your Data

1. **Rate limiting & abuse prevention** — IP + window counters in D1
2. **Malware checks** — SHA-256 looked up against AlienVault OTX by default, plus optional MalwareBazaar / VirusTotal and local blocklists
3. **Service operation** — storing files, serving links, expiry cleanup
4. **Account features** — dashboard, albums, delete control
5. **Legal compliance** — responding to valid DMCA/abuse reports

---

## Data Sharing

| Recipient | Data Shared | Reason |
|-----------|-------------|--------|
| **AlienVault OTX** | File SHA-256 hash only | Default malware reputation lookup |
| **MalwareBazaar (abuse.ch, optional)** | File SHA-256 hash only | Malware lookup |
| **VirusTotal (optional)** | File SHA-256 hash only | Secondary malware lookup |
| **Telegram (private channel)** | File content and basic metadata | Storage for permanent files up to 20 MB |
| **Cloudflare** | All traffic (TLS termination, DDoS, cache) | Infrastructure provider |
| **Authorities (valid legal request)** | Uploader IP, file metadata, timestamp | DMCA, law enforcement |

**We do not sell, rent, or share data for advertising, analytics, or marketing.**

---

## Your Rights

| Right | How to Exercise |
|-------|-----------------|
| **Access your data** | Email `meowboxteam@gmail.com` with your username/IP |
| **Delete your files** | Use dashboard (`/manage`) or API `deletefiles` with your `userhash` |
| **Delete your account** | Email `meowboxteam@gmail.com` — manual process (no self-serve yet) |
| **Opt out of malware checks** | Not possible — hash reputation checks run on all uploads |
| **Object to processing** | Email `meowboxteam@gmail.com` |

---

## Retention Schedule

| Data | Retention | Deletion Trigger |
|------|-----------|------------------|
| Uploader IP in file metadata | Until file deleted or expires | File deletion or expiry cleanup |
| Uploader IP in rate counters | Rolling window | Opportunistic purge of `rate2` windows older than 120 windows |
| File metadata (DB) | Until file deleted or expires | Cron purges expired files; manual delete on request |
| Malware cache (KV) | 30 days | TTL auto-expires |
| Session cookie | 30 days from last login | Expires or logout |
| Crawl logs | 90 days | Manual cleanup (low volume) |
| Account data | Until account deletion | Manual on request |

---

## Security Measures

- HTTPS everywhere, 1-year HSTS, strict CSP
- Passwords: PBKDF2-SHA256, 100k iterations, 16-byte salt
- Session cookies: HttpOnly, Secure, SameSite=Lax, 30-day TTL
- Passwords never logged, never in URLs
- Malware check cache isolated in KV (no file content stored)
- Fail-open lookups: service stays up even if reputation providers are down

---

## International Transfers

All processing occurs on Cloudflare's global network. Data may traverse Cloudflare's edge locations worldwide. Subprocessors are Cloudflare, AlienVault OTX, optional MalwareBazaar/VirusTotal, and Telegram for files stored in the private backup channel.

---

## Children's Privacy

MeowBox is not directed at children under 13. We do not knowingly collect data from children. If you believe a child has uploaded data, contact us for deletion.

---

## Changes to This Policy

Updates posted here with new effective date. Material changes announced via repository `CHANGELOG.md` and site banner.

---

## Contact

- **Email**: `meowboxteam@gmail.com`
- **Security issues**: [GitHub Security Advisories](https://github.com/BhagattJii/meowbox/security/advisories/new)
- **DMCA / Abuse**: `meowboxteam@gmail.com` (include direct link `/f/xxxxxx`)

---

*This policy covers the MeowBox service at `https://meowbox.dpdns.org` and its API. The documentation repository (`github.com/BhagattJii/meowbox`) is public and collects no personal data.*