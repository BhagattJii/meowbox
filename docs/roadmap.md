# MeowBox Roadmap

Planned features, improvements, and milestones. Items are not guaranteed — priorities shift based on capacity and feedback.

---

## ✅ Completed (v1.0 – 2026-10)

- [x] Core upload & direct links (`/f/xxxxxx`)
- [x] Anonymous uploads, no signup required
- [x] Expiring links (2 h / 24 h / 2 d / 7 d) + permanent default
- [x] Malware scanning (MalwareBazaar + VirusTotal)
- [x] Free accounts: dashboard, albums, delete control
- [x] REST API (`/user/api.php`) with 8 `reqtype` actions
- [x] Rate limits (upload, view, login, signup)
- [x] SEO: sitemap, IndexNow, JSON-LD, redirects, security.txt, browserconfig
- [x] Landing page `/free-file-sharing` with FAQ schema
- [x] Documentation repo (this repo) with full API/limits/architecture docs

---

## 🎯 Near Term (Q4 2026 – Q1 2027)

### Core Features
- [ ] **WebP auto-conversion** — upload JPEG/PNG → serve WebP via `Accept` header (KV transform or Cloudflare Images)
- [ ] **Folder upload** — zip multiple files, single link to folder index
- [ ] **WebDAV endpoint** — mount MeowBox as a network drive
- [ ] **Client SDKs** — Python, Go, Node.js, Rust (thin wrappers around `/user/api.php`)

### UX & Frontend
- [ ] **Drag-and-drop progress bar** with real-time speed/ETA
- [ ] **Dark/light theme toggle** (persisted in localStorage)
- [ ] **Copy-to-clipboard button** on upload success
- [ ] **QR code** for direct link (mobile sharing)

### API Enhancements
- [ ] **Batch upload** — single `reqtype` accepting multiple files
- [ ] **Presigned upload URLs** — client-side direct-to-storage (bypass Worker for large files)
- [ ] **Webhook callbacks** — `POST` to user URL on upload/delete/expiry
- [ ] **OpenAPI 3.0 spec** + Swagger UI at `/api/docs`

### Accounts & Auth
- [ ] **Email verification** (optional, for password reset)
- [ ] **Password reset flow** (email token → new password)
- [ ] **2FA (TOTP)** for account security
- [ ] **API keys** (scoped, revocable) instead of raw `userhash`

---

## 🚀 Medium Term (2027 H1)

### Storage & Performance
- [ ] **R2 migration** — move remote store to Cloudflare R2 (native, cheaper, no Telegram dependency)
- [ ] **Streaming uploads** — chunked upload for > 25 MB (if limit raised)
- [ ] **Edge caching tuning** — per-file `Cache-Control` based on popularity
- [ ] **Global KV replication** — ensure low latency worldwide (already edge, but monitor)

### Admin & Moderation
- [ ] **Admin dashboard** (internal) — global stats, abuse queue, storage usage
- [ ] **Automated DMCA workflow** — report → queue → takedown → notify
- [ ] **Abuse scoring** — per-IP / per-user risk score, auto-throttle
- [ ] **Audit log** — admin actions, deletions, config changes

### Monetization (Optional, Non-Intrusive)
- [ ] **Voluntary donations** (Crypto/Stripe) — no feature gating
- [ ] **Sponsored link** on homepage (clearly labeled, opt-out via header)
- [ ] **Custom domain for albums** (e.g., `albums.yourdomain.com` → CNAME to MeowBox)

---

## 🌱 Long Term / Vision (2027+)

### Platform
- [ ] **Plugin system** — community upload processors (virus scan, transcoding, OCR)
- [ ] **Federation** — ActivityPub for file sharing across instances
- [ ] **P2P fallback** — WebRTC/WebTorrent for popular files (reduce origin load)
- [ ] **AI-powered features** — auto-caption images, transcript audio, summarize PDFs

### Ecosystem
- [ ] **Official CLI** (`meowbox` binary) with config, aliases, progress bars
- [ ] **VS Code / JetBrains extension** — right-click → upload to MeowBox
- [ ] **Mobile app** (iOS/Android) — native share sheet integration
- [ ] **Browser extension** — right-click image/link → "Send to MeowBox"

### Governance
- [ ] **Open-source core** (Worker + D1 schema) under MIT/Apache-2
- [ ] **Community contributors** — issue triage, docs, SDKs
- [ ] **Transparent roadmap** — public project board, RFC process

---

## Deprecation Policy

- **API changes**: 90-day notice via `CHANGELOG.md`, GitHub releases, and `X-API-Deprecation` header
- **Feature removal**: Only for security/legal reasons; migration path provided
- **Link format**: `/f/<short>` is permanent — never changed

---

## How to Contribute Ideas

- Open a **Feature Request** issue in this repo (use the template)
- Join discussions on existing issues
- Submit a PR to `docs/ROADMAP.md` with your proposal
- Email `meowboxteam@gmail.com` for private suggestions

---

## Versioning

| Version | Target | Highlights |
|---------|--------|------------|
| v1.0 | 2026-10 | Launch — core features, SEO, docs |
| v1.1 | 2026-Q4 | WebP, folder upload, WebDAV, SDKs |
| v1.2 | 2027-Q1 | R2 migration, streaming, admin dash |
| v2.0 | 2027+ | Federation, P2P, AI features |

---

*Roadmap is a living document. Star this repo to watch for updates.*