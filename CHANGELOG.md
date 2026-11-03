# Changelog

All notable changes to the MeowBox documentation and service are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-10-30

### Service Launch
- Core file upload & direct links (`/f/xxxxxx`)
- Anonymous uploads (no signup required)
- Expiring links: 2 h / 24 h / 2 d / 7 d + permanent default
- Malware scanning (MalwareBazaar + optional VirusTotal)
- Free accounts: dashboard, albums, delete control
- REST API (`/user/api.php`) with 8 `reqtype` actions
- Rate limits: upload, view, login, signup
- Storage tiers: Cloudflare KV + remote object store
- Cron purge (every 15 min) for expired files & sessions
- HTTPS everywhere, HSTS 1y, strict CSP, security headers

### SEO & Discovery
- Sitemap.xml (10 URLs, `lastmod` on deploy)
- IndexNow automatic submission on deploy
- JSON-LD: Organization, WebSite, WebApplication, SoftwareApplication, HowTo, FAQPage, BreadcrumbList
- Redirects: `*.workers.dev` & `www` → canonical (301 + `X-Robots-Tag: noindex, nofollow`)
- `robots.txt`, `browserconfig.xml`, `.well-known/security.txt`
- Canonical URLs, Open Graph, Twitter Cards, msapplication tiles

### Documentation (This Repo)
- Professional README with badges, quick start, links
- `docs/HOW-IT-WORKS.md` — architecture, request lifecycle, storage, scanning, limits
- `docs/API.md` — full API reference with curl examples
- `docs/LIMITS.md` — complete limits table with rationale
- `docs/FAQ.md` — 20+ questions answered
- `docs/ARCHITECTURE.md` — tech stack, data model, storage tiers, scanning, cron, security boundaries
- `docs/PRIVACY.md` — data collected, retention, rights, contact
- `docs/SEO.md` — sitemap, IndexNow, JSON-LD, meta tags, monitoring checklist
- `docs/ROADMAP.md` — planned features through 2027+
- `docs/DEPLOYMENT.md` — how to deploy your own instance
- `docs/SUPPORT.md` — help channels, bug/feature templates, abuse/security reporting
- `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`, `CHANGELOG.md`
- GitHub issue templates (bug, feature), PR template, dependabot config

---

## [Unreleased]

### Planned (see Roadmap)
- WebP auto-conversion
- Folder upload (zip → folder index)
- WebDAV endpoint
- Client SDKs (Python, Go, Node, Rust)
- R2 migration (replace remote store)
- Admin dashboard
- OpenAPI 3.0 spec + Swagger UI
- Email verification / password reset / 2FA
- API keys (scoped, revocable)

---

## Versioning Notes

- **Service version** ≠ **Docs repo version** — the service is continuously deployed; docs versions mark documentation milestones.
- Breaking API changes: 90-day notice via `CHANGELOG.md`, GitHub releases, and `X-API-Deprecation` header.
- Link format `/f/<short>` is permanent — never changed.