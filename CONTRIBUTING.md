# Contributing to MeowBox

MeowBox is a free, ad-free file host. This repository contains **documentation only** — the service source code is not published here. Contributions to documentation, issue reports, and feature suggestions are very welcome.

---

## How to Contribute

### 1. Report a Problem
Open a **Bug Report** issue (use the template) and include:
- Affected URL or API `reqtype`
- Steps to reproduce (numbered)
- Expected vs actual behavior
- Error message / HTTP status
- Browser / `curl` version / User-Agent
- **Remove API keys, tokens, `userhash`, session cookies, and file contents before pasting anything.**

### 2. Request a Feature
Open a **Feature Request** issue (use the template) and describe:
- The problem you're trying to solve
- Your proposed solution (or "I'm not sure, but…")
- Alternatives you've considered
- Who benefits and how often

### 3. Improve Documentation
- Fix typos, clarify wording, add missing details
- Add examples to `docs/API.md` or `docs/FAQ.md`
- Update `README.md` if you change a user-facing feature
- Keep style: Markdown, American English, concise, scannable

### 2. Pull Requests
1. One logical change per PR
2. Describe the change and why it matters
3. Link related issues (`Fixes #123`)
4. Run the docs check locally: `python3 scripts/check_docs_links.py` (if available)
5. Fill in the PR template checklist

---

## Ground Rules (Service Principles)

These principles guide the MeowBox service and its documentation:

- **No ads, trackers, analytics pixels, or third-party scripts.** The service is funded by nobody and tracks nobody.
- **No secrets in the repo.** API keys, upload tokens, and certificates stay in server-side environment variables.
- **Uploads must keep passing the malware scan.** Never weaken the signature checks or the banned-file-type list.
- **Keep uploads anonymous by default.** Account features are additive, never a requirement.
- **Do not commit uploaded user files, database dumps, or operational credentials.**

---

## Documentation Style Guide

- **Language**: American English
- **Format**: Markdown (GitHub-flavored)
- **Tone**: Concise, direct, professional
- **Structure**: Headings → short paragraphs → tables/lists for scannability
- **Links**: Relative for internal (`docs/API.md`), absolute for external
- **Code blocks**: Use for curl examples, JSON, config — not for prose
- **Tables**: Prefer tables for limits, API fields, error codes
- **Emphasis**: `**bold**` for UI elements, `code` for technical terms

---

## Security Issues

**Do not open a public issue.** Report privately via GitHub Security Advisories:

https://github.com/BhagattJii/meowbox/security/advisories/new

See [SECURITY.md](SECURITY.md) for full policy.

---

## License

By contributing you agree that your contributions are licensed under the MIT license of this repository (see [LICENSE](LICENSE)).

---

## Questions?

- Open a **Discussion** (if enabled) or email `meowboxteam@gmail.com`
- Check existing issues and the [FAQ](docs/FAQ.md) first