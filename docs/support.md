# MeowBox Support & Reporting

## Getting Help

| Channel | Best For | Response Time |
|---------|----------|---------------|
| **GitHub Issues** | Bug reports, feature requests, documentation fixes | 1–7 days |
| **Email** (`meowboxteam@gmail.com`) | Account help, DMCA, abuse, business inquiries | 1–3 days |
| **Security Advisories** | Vulnerability reports (do not use public issues) | 72 hours acknowledgment |

---

## Before Opening an Issue

1. **Search existing issues** — your problem may already be reported.
2. **Check the FAQ** — [docs/FAQ.md](faq.md) covers 20+ common questions.
3. **Reproduce minimally** — note the exact steps, URL, and error message.
4. **Remove secrets** — never paste API keys, `userhash`, session cookies, or file contents.

---

## Reporting a Bug

Use the **Bug Report** template (auto-filled when you click "New Issue → Bug report").

**Required information**:
- Affected URL or API `reqtype`
- Steps to reproduce (numbered)
- Expected vs actual behavior
- Error message or HTTP status
- Browser / `curl` version / User-Agent
- Time (UTC) if time-sensitive

**Do not include**: API keys, `userhash`, session cookies, uploaded file contents.

---

## Requesting a Feature

Use the **Feature Request** template.

**Helpful details**:
- Problem you're trying to solve
- Proposed solution (or "I don't know, but it would be nice if…")
- Alternatives considered
- Impact (who benefits, how often)

---

## Reporting Abuse / DMCA

**Email**: `meowboxteam@gmail.com`

**Include**:
- Direct link(s): `https://meowbox.dpdns.org/f/xxxxxx`
- Nature of abuse (malware, copyright, illegal content, spam, phishing)
- Your contact info (for follow-up)
- For DMCA: identification of copyrighted work, location, good-faith statement, signature

We act on valid reports promptly. False reports may be forwarded to the uploader.

---

## Reporting a Security Vulnerability

**Do not open a public issue.**

Use **GitHub Security Advisories**:
https://github.com/BhagattJii/meowbox/security/advisories/new

**Include**:
- Affected endpoint / component
- Reproduction steps (minimal)
- Impact assessment (data exposure, RCE, auth bypass, etc.)
- Suggested fix (if any)

**Expect**: acknowledgment within 72 hours, status updates until resolution.

---

## Account Support

| Issue | How to Resolve |
|-------|----------------|
| Forgot password | No self-serve reset yet — email `meowboxteam@gmail.com` |
| Lost `userhash` | Check registration email / dashboard; else email support |
| Delete account | Email `meowboxteam@gmail.com` (manual process) |
| Change email/username | Not supported yet — delete & re-register |
| 2FA / API keys | Not implemented yet — see [Roadmap](roadmap.md) |

---

## API Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `403 invalid userhash` | Typo / expired / wrong account | Re-copy from dashboard or registration response |
| `429 slow down` | Rate limit hit | Wait, reduce frequency, check [limits](limits.md) |
| `413 file too large` | > 25 MB (GIF > 20 MB) | Compress / convert to WebM |
| `403 file blocked` | Malware signature / banned ext | File is malicious or disallowed |
| `410 Gone` | Link expired or file deleted | Re-upload with desired TTL |
| `503 capacity` | KV soft cap + remote store down | Retry later; service auto-recovers |

---

## Service Status

- **No public status page** (free service, best-effort)
- Check [GitHub Issues](https://github.com/BhagattJii/meowbox/issues) for ongoing incidents
- Monitor `https://meowbox.dpdns.org/` — if it loads, core service is up

---

## Community

- **GitHub Discussions** — not enabled (low volume)
- **Social** — Instagram [@i.lakshyy](https://www.instagram.com/i.lakshyy) (owner)
- **Email** — `meowboxteam@gmail.com`

---

## For Contributors

- **Docs only** — this repo contains documentation, not service source
- **Style** — Markdown, American English, concise, scannable
- **PR checklist** — see [CONTRIBUTING.md](CONTRIBUTING.md)
- **Code of Conduct** — see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

---

## Response Time Commitments

| Type | Target |
|------|--------|
| Security advisory acknowledgment | ≤ 72 hours |
| Abuse / DMCA email | ≤ 48 hours |
| Bug report (critical) | ≤ 7 days |
| Feature request / docs | ≤ 14 days |
| General email | ≤ 5 days |

*This is a free, best-effort service — no SLA, no guaranteed uptime.*

---

## Escalation

If you don't receive a response within the target window:
1. Reply to the same thread/email
2. Mention "ESCALATION" in subject
3. If still no response, the service may be experiencing high volume or the maintainer is unavailable — patience appreciated.

---

*Thank you for using MeowBox. Your reports make the service better for everyone.*