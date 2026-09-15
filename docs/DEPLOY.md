# Deploy — richoffpints.com

Operator runbook for the official ICEWEAR VEZZO — ROP 4 campaign site.

Live URL: https://richoffpints.com
Repo: https://github.com/DigitalCurrensy/ICEWEAR-VEZZO-ROP4-WEBSITE

This file is for people who ship the site. Fans should start at the root [README](../README.md).

---

## What ships

The public site is static HTML.

| Input | Output |
| --- | --- |
| `index.html` in git (source of record in this repo) | `public/index.html` after `build.sh` |
| `vercel.json` | Vercel build settings |
| Higgsfield-hosted images, video, and game | Loaded by the browser at request time |

There is no Node app, no database, and no public API on this domain.

---

## Vercel

- Project name in the dashboard: `rop4-lead-api`
- Team: DIGITAL CURRENSY INC
- Framework: none
- Install command: empty
- Build command: `bash build.sh`
- Output directory: `public`

`vercel.json` must stay in the **repo root**. An earlier setup stored build config only in the dashboard. Clicking Redeploy then rebuilt an empty tree and the live domain returned 404. Committing the file makes Redeploy deterministic.

Current file:

```json
{
  "buildCommand": "bash build.sh",
  "outputDirectory": "public",
  "installCommand": "",
  "framework": null
}
```

No production environment variables are required for the public page. CMS keys, if used at all, stay on a local machine.

---

## build.sh

`build.sh` does two jobs:

1. Fetch the approved HTML into `public/index.html`.
2. Refuse to publish if required campaign links are missing or known-bad assets reappear.

Canonical fetch URL inside the script:

`https://upload.higgsfield.ai/user_36SLpLHo0MVI10STslhM0wOZWEK/a8a7c0a4-6953-47ab-af21-41ee391b33e2.html`

After download, the script rewrites that source URL to `https://richoffpints.com/` so share cards and self-links point at the live domain.

### Guards

Counts use `grep -o | wc -l` (occurrences), never `grep -c` (matching lines). Several hits on one line would undercount with `grep -c` and fail a good build.

| Check | Expected | Why |
| --- | --- | --- |
| `blue-cloud-787` | 6 | Every game link still points at Higgsfield |
| `5SHpv38Vz3I` | 3 | YouTube embed + poster + Watch button |
| `43b44897` | 0 | Wrong mp4 must stay gone |
| `paged.net` | 0 | Dead game host must stay gone |
| `21c116c7` | 0 | Wrong background video must stay gone |
| `3e1eb56b` | 1 | Correct silent hero video |
| `richoffpints.com` | present | Live domain appears in the page |

If any check fails, the script exits non-zero. Vercel keeps serving the last good deployment.

Run the same checks locally:

```bash
bash build.sh
ls -l public/index.html
```

`public/` is gitignored. It is a build artifact, not source.

---

## Local preview

Day-to-day preview does not need Vercel:

```bash
python3 -m http.server 4173
```

Open `http://127.0.0.1:4173/index.html`.

The game still loads from `https://blue-cloud-787.higgsfield.gg/`. That is expected.

---

## Content publishing helper

`cms/` is optional. It does not deploy the site and it does not write `index.html`.

Flow:

1. Draft a drop fixture.
2. A named human approves it.
3. A named human publishes it.

Missing `PAYLOAD_URL` or `PAYLOAD_TOKEN` stops the command. Live tokens never belong in git.

```bash
python3 cms/payload_wrap.py --draft cms/fixtures/the-drop.draft.json
python3 cms/payload_wrap.py --approve the-drop --actor-name YOUR_NAME
python3 cms/payload_wrap.py --publish the-drop --actor-name YOUR_NAME
python3 cms/tests/test_payload_wrap.py
```

See [cms/CMS_LOCK.md](../cms/CMS_LOCK.md).

---

## Do not

- Put API keys, Payload tokens, or `.env` files in git.
- Base64-encode video.
- Use a data URI for `og:image`.
- Point game links at any host other than `blue-cloud-787.higgsfield.gg` / `.app`.
- Remove `vercel.json` from the repo root.
- Let a helper script overwrite `index.html` or `build.sh`.

---

## Related

- Live site: https://richoffpints.com
- Game: https://blue-cloud-787.higgsfield.gg/
- Official game repo: https://github.com/DigitalCurrensy/ICEWAER-VEZZO-ROP4-VIDEO-GAME-OFFICIAL
- Album smart link: https://foundation-media.ffm.to/rop4
- Official visual: https://youtu.be/5SHpv38Vz3I
