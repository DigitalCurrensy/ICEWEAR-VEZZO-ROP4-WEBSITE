# ICEWEAR VEZZO — ROP 4 (Rich Off Pints 4)

Campaign microsite for the ROP 4 album + playable game.
Live: **https://richoffpints.com**

## Contents

| File | Purpose |
|---|---|
| `index.html` | The entire site — single file, no build step, no dependencies |
| `vercel.json` | Vercel build config. **Must stay in the repo root** (see below) |
| `build.sh` | Build + content guards |

## Deploying

Vercel project: `rop4-lead-api` (team: DIGITAL CURRENSY INC).
Static single file — no framework, no install step, no env vars.

`vercel.json` lives in the tree on purpose. An earlier deploy kept its build
config only inside the deployment, so clicking **Redeploy** in the dashboard
rebuilt an empty tree and served a 404. With the config committed here, a
redeploy reproduces the site correctly.

`build.sh` asserts on content before publishing — a wrong build fails instead
of shipping, and a failed build never takes the live site down (Vercel keeps
serving the last good deployment).

## The site

- Hero background video: 568×320 master, blurred + scrimmed as atmosphere.
  Audio stream stripped entirely (`-an`), so it cannot make sound.
  `src` is set in JS so `prefers-reduced-motion` never downloads it.
- Game portal: embeds https://blue-cloud-787.higgsfield.gg/ inline on desktop,
  opens in a new tab on touch.
- If a host blocks the embed (chat previews, CMS embeds), the poster and Play
  button are restored rather than leaving a dead frame. The poster is only
  removed once the game proves it loaded.
- No forms, no email capture, no backend, no analytics endpoints.

## Assets

Images and audio are inlined as base64 or served from Higgsfield's CDN.
Video is always hosted — never base64 (it inflates ~33% and blocks first paint).

`og:image` must always be an absolute https URL, never a data URI — crawlers
fetch it from their own servers, so base64 means no share card at all.
