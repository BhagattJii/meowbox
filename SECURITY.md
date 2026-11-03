# Security Policy

## Reporting a Vulnerability

**Do not open a public issue.** Report privately via GitHub Security Advisories:

https://github.com/BhagattJii/meowbox/security/advisories/new

**Include**:
- Affected endpoint / component
- Minimal reproduction steps
- Impact assessment (data exposure, RCE, auth bypass, etc.)
- Suggested fix (if any)

**Expect**: acknowledgment within **72 hours**, status updates until resolution.

---

## Supported Versions

This repository contains **documentation only** — the service source code is not published here. Security policies apply to the live service at `https://meowbox.dpdns.org`.

| Version | Supported |
|---------|-----------|
| Current (continuously deployed) | ✅ |

---

## Scope & Threat Model

MeowBox accepts untrusted uploads from anonymous users and serves them back over direct links. The critical attack surfaces are:

| Area | Threats |
|------|---------|
| **Upload validation** | Path traversal, filename injection, MIME/type sniffing bypass, banned file types bypass |
| **Malware scanning** | Storing a file whose signature was rejected; cache poisoning |
| **Direct links / hotlinking** | Access-control bypass on `/f/*`, expired files served (should be `410 Gone`) |
| **API (`/user/api.php`)** | Broken auth on `deletefiles`/album endpoints, `userhash` guessing/reuse, CSRF |
| **Infrastructure** | SSRF in `urlupload`, SQL injection, path traversal in album/cover handling, rate-limit bypass |
| **Privacy** | Any tracking, analytics, or third-party request carrying user data |

---

## Security Controls in Place

| Control | Implementation |
|---------|----------------|
| **Upload validation** | Extension allowlist, magic-byte block (MZ/ELF), size clamp, filename sanitization |
| **Malware scanning** | SHA-256 → MalwareBazaar + optional VirusTotal, 30-day KV cache, fail-open |
| **Direct link access** | No auth (by design), `410 Gone` on expiry, `cache-control: no-cache`, purge on delete |
| **API auth** | Session cookie **OR** `userhash` form field; `userhash` validated against `users` table |
| **Delete authorization** | `owner == userhash` enforced per file; album ownership checked per album |
| **Rate limits** | Edge-enforced via D1 counters + in-memory flood guard (see [limits](docs/LIMITS.md)) |
| **CORS** | `access-control-allow-origin: *` on API and served files |
| **Security headers** | `nosniff`, `cross-origin-resource-policy: cross-origin`, HSTS 1y, `referrer-policy: no-referrer` |
| **CSP on HTML** | `default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; font-src 'self'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'` |
| **Secrets management** | All secrets in Cloudflare Worker secrets (`BOT_TOKEN`, `MB_AUTHKEY`, `VT_API_KEY`); never in repo |

---

## Out of Scope

- Attacks requiring compromise of Cloudflare infrastructure
- Attacks requiring compromise of Telegram / remote object store
- Social engineering of the maintainer
- Denial-of-service beyond Cloudflare's protection

---

## Disclosure Timeline

| Milestone | Target |
|-----------|--------|
| Acknowledgment | ≤ 72 hours |
| Initial assessment | ≤ 7 days |
| Fix developed & tested | ≤ 30 days (critical), ≤ 90 days (non-critical) |
| Deploy & disclosure | Coordinated with reporter |

---

## Recognition

Reporters of valid vulnerabilities (with coordinated disclosure) will be acknowledged in `CHANGELOG.md` and a `SECURITY` hall-of-fame (unless anonymity requested).

---

## Contact

- **Security advisories**: https://github.com/BhagattJii/meowbox/security/advisories/new
- **Email**: `meowboxteam@gmail.com` (for non-vulnerability security questions)
- **PGP**: Not currently published — use Security Advisories for sensitive reports

---

*This policy covers the MeowBox service at `https://meowbox.dpdns.org` and its API. This documentation repository (`github.com/BhagattJii/meowbox`) is public and contains no operational secrets.*