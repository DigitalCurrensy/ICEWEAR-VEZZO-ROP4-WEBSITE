# Security

Report a vulnerability privately with a GitHub Security Advisory on this repository
(Security, then Report a vulnerability). Do not open a public issue for a secret,
a credential, or a vulnerability that is still unfixed.

Do not commit secrets. Database URLs and API keys belong in the shell or in a
sops-encrypted `*.enc.env` file. The private age key stays on the machine that
created it (`~/.config/sops/age/keys.txt`) and is never committed.

`.gitleaks.toml` flags `DATABASE_URL` values and API key assignments. Pre-commit
and CI both run that config.

Agents draft. Humans approve and send. Nothing in the hygiene workflow merges
a pull request or publishes a release.
