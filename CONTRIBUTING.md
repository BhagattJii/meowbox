# Contributing to MeowBox

MeowBox is a free, ad-free file host. Contributions that keep it that way are very welcome.

## Report a problem

Open an issue and include the affected URL or API `reqtype`, the steps to reproduce, and the relevant response output. **Remove API keys, tokens and user file contents before pasting anything.**

## Ground rules

- **No ads, trackers, analytics pixels or third-party scripts.** The service is funded by nobody and tracks nobody.
- **No secrets in the repo.** API keys, upload tokens and certificates stay in server-side environment variables.
- **Uploads must keep passing the malware scan.** Never weaken the signature checks or the banned-file-type list.
- **Keep uploads anonymous by default.** Account features are additive, never a requirement.
- **Do not commit uploaded user files or database dumps.**

## Pull requests

1. One logical change per PR.
2. Describe how you verified it (manual steps are fine).
3. Update the README if you changed an API `reqtype` or added a limit.
4. Fill in the PR template checklist.

## Security issues

Do not open a public issue — see [SECURITY.md](SECURITY.md).

## License

By contributing you agree that your contributions are licensed under the MIT license of this repository.
