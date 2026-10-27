# Security Policy

## Reporting a vulnerability

**Do not open a public issue.** Report it privately through GitHub Security Advisories:

https://github.com/BhagattJii/meowbox/security/advisories/new

Include the affected endpoint, reproduction steps and impact. Expect an acknowledgement within 72 hours.

## Scope

MeowBox accepts untrusted uploads from anonymous users and serves them back over direct links, so the areas that matter most are:

- **Upload validation** — path traversal, filename injection, MIME/type sniffing bypass, banned file types getting through
- **Malware scanning** — ways to store a file whose signature was rejected
- **Direct links / hotlinking** — access-control bypass on `/f/*` URLs, expired files still being served (expected response is `410 Gone`)
- **API (`/user/api.php`)** — broken authentication on `deletefiles` / album endpoints, `userhash` guessing or reuse
- **Infrastructure** — SSRF in `urlupload`, SQL injection, path traversal in album/cover handling, rate-limit bypass
- **Privacy** — any tracking, analytics or third-party request carrying user data

## Notes

- The uploader IP is retained for anti-abuse (malware / DMCA reports). This is documented on the site's legal page.
- Deletion of anonymous uploads requires the `userhash` returned at upload time.
