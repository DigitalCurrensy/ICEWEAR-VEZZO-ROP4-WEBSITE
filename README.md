# ICEWEAR VEZZO — ROP 4

Official campaign site for **Rich Off Pints 4** — the album, the official visual, and the playable 6 Mile Night Run.

**Live site:** [https://richoffpints.com](https://richoffpints.com)

[Play the game](https://blue-cloud-787.higgsfield.gg/) · [Stream the album](https://foundation-media.ffm.to/rop4) · [Watch the visual](https://youtu.be/5SHpv38Vz3I)

![ROP 4 — album + playable game](https://upload.higgsfield.ai/user_36SLpLHo0MVI10STslhM0wOZWEK/2244481a-643d-4139-b03b-ec907f39fadb.jpg)

Detroit. Album + playable game. Out now. Presented by **Iced Up Records** and **Foundation Media**.

---

## What this site is

[richoffpints.com](https://richoffpints.com) is a single-page campaign site. No account. No signup. No forms.

Fans land here to do three things:

1. **Play** the ROP 4 night run
2. **Watch** the official visual
3. **Stream** Rich Off Pints 4

| Go here | What you get |
| --- | --- |
| [richoffpints.com](https://richoffpints.com) | Official album + game hub |
| [Play 6 Mile Night Run](https://blue-cloud-787.higgsfield.gg/) | Fullscreen game |
| [Listen now](https://foundation-media.ffm.to/rop4) | Album on every major platform |
| [Official visual](https://youtu.be/5SHpv38Vz3I) | ROP 4 world on YouTube |
| [Game repo](https://github.com/DigitalCurrensy/ICEWAER-VEZZO-ROP4-VIDEO-GAME-OFFICIAL) | How to play, screenshots, campaign record |

---

## Screenshots

### The game — 6 Mile Night Run

Drive the white ROP 4 sedan through night traffic. Collect Purple Pints. Hit Perfect Dodges. Fire Purple Boost. Post your rank.

![6 Mile Night Run — white sedan, Detroit night](https://d8j0ntlcm91z4.cloudfront.net/user_36SLpLHo0MVI10STslhM0wOZWEK/hf_20260709_091202_d1a6f37d-5a5b-49cc-b979-4fc2afdeb792.png)

Free to play. No signup. One run is about one minute.

### The album

![Rich Off Pints 4 cover](https://upload.higgsfield.ai/user_36SLpLHo0MVI10STslhM0wOZWEK/448ebc5f-d319-4b75-a9a6-d5cb00765fe7.png)

15 tracks. Released July 17, 2026 on Iced Up Records. Features include Payroll Giovanni, GT, 42 Dugg, Montana 700, Peezy, and Pistol Po.

### The world

Garage light, iced detail, pink fit, white trucks, flash-photo energy.

<p>
<img src="https://upload.higgsfield.ai/user_36SLpLHo0MVI10STslhM0wOZWEK/121af15b-f735-4e63-b42b-ebebbb2d09b5.png" alt="Icewear Vezzo — pink fit, white trucks" width="48%" />
&nbsp;
<img src="https://upload.higgsfield.ai/user_36SLpLHo0MVI10STslhM0wOZWEK/b2e7cecd-6677-4852-b0b5-2829969c9e21.jpg" alt="Icewear Vezzo — G-Wagon still" width="48%" />
</p>

<p>
<img src="https://upload.higgsfield.ai/user_36SLpLHo0MVI10STslhM0wOZWEK/f363ab89-c438-4eb1-b4e9-bbe1ae073d15.jpg" alt="Cafe 1923 — IUR Road Runner" width="48%" />
&nbsp;
<img src="https://i.ytimg.com/vi/5SHpv38Vz3I/maxresdefault.jpg" alt="Official visual — white luxury coupe at night" width="48%" />
</p>

---

## What is on the page

The live site is one HTML file. Five public sections:

| Section | Title | What it does |
| --- | --- | --- |
| 01 The Run | Play Rich Off Pints 4 | Embeds the Higgsfield game on desktop. Opens the full game in a new tab on phones. |
| 02 The Visuals | Watch the ROP 4 World | Plays the official YouTube visual (`5SHpv38Vz3I`). |
| 03 The Album | Play ROP 4 Your Way | Sends listeners to the Foundation Media smart link. |
| 04 The World | ROP 4: The World | Still gallery — Detroit, chrome, garage light, midnight speed. |
| 05 The Game | Luxury Night Run | Explains the 60-second loop in four beats. |

Follow row at the bottom:

- [Instagram](https://www.instagram.com/icewear_vezzo)
- [TikTok](https://www.tiktok.com/@icewear.vezzo6)
- [X](https://x.com/icewear_vezzo)
- [YouTube](https://www.youtube.com/channel/UC00wbhsfrcZAElIw1Q9VRlw)
- [Kick](https://kick.com/icewear-vezzo)
- [Spotify](https://open.spotify.com/artist/1ZbmerOthZbxz5eR3c9Mn1)
- [Apple Music](https://music.apple.com/us/artist/icewear-vezzo/514871285)

---

## How the game is embedded

The playable build is hosted on Higgsfield, not inside this repo.

- Desktop: the site loads `https://blue-cloud-787.higgsfield.gg/` in an inline frame after the visitor hits Play.
- Touch devices: the same URL opens in a new tab so the game can use the full screen.
- If an embed host blocks the frame, the poster and Play button stay visible instead of a dead box.
- The poster is removed only after the game actually loads.

Full play guide: [ICEWAER-VEZZO-ROP4-VIDEO-GAME-OFFICIAL](https://github.com/DigitalCurrensy/ICEWAER-VEZZO-ROP4-VIDEO-GAME-OFFICIAL).

The GitHub repo name has a historical typo (`ICEWAER`). The official spelling is **Icewear**.

---

## What is in this repo

| Path | Purpose |
| --- | --- |
| `index.html` | The whole public site. No framework. No npm install. |
| `vercel.json` | Tells Vercel how to build. Must stay in the repo root. |
| `build.sh` | Copies the approved HTML into `public/` and checks required content before publish. |
| `cms/` | Optional local draft → human-approve → publish helper. Does not write the live page. |
| `docs/DEPLOY.md` | Operator runbook. |
| `LICENSE` | Brand and code rights. |

This repo does **not** contain the game engine, the soundtrack masters, or a leaderboard database. Those live on Higgsfield and the music platforms.

---

## Preview locally

No build step for day-to-day preview:

```bash
# from the repo root
python3 -m http.server 4173
# open http://127.0.0.1:4173/index.html
```

Or open `index.html` directly in a browser. The game iframe still points at the live Higgsfield URL.

---

## Deploy

Vercel project: `rop4-lead-api` (team: DIGITAL CURRENSY INC).

The site is static. No runtime env vars are required for the public page.

`vercel.json` is committed on purpose. If the build config only existed in the Vercel dashboard, a dashboard Redeploy rebuilt an empty tree and served a 404. With the file in git, Redeploy reproduces the live site.

`build.sh` fails the deploy when required links are missing. A failed build does not take the live site down — Vercel keeps the last good deployment.

```bash
bash build.sh
```

Guards count *occurrences*, not matching lines (`grep -o | wc -l`, never `grep -c`). That matters when several hits share one line.

Full operator notes: [docs/DEPLOY.md](docs/DEPLOY.md).

---

## Publishing extra copy (optional)

The live page is `index.html`. The `cms/` folder is a separate helper for a single content collection called **The Drop**.

Rules, in plain English:

1. An agent or a person can draft.
2. A named human must approve (`--actor-name` is required).
3. A named human must publish.
4. Missing local CMS URL or token stops the command. Nothing is published by accident.
5. Live keys stay out of git. Use `.env` locally. `.env.example` is placeholders only.
6. The helper never overwrites `index.html` or `build.sh`.

```bash
python3 cms/payload_wrap.py --draft cms/fixtures/the-drop.draft.json
python3 cms/payload_wrap.py --approve the-drop --actor-name YOUR_NAME
python3 cms/payload_wrap.py --publish the-drop --actor-name YOUR_NAME
python3 cms/tests/test_payload_wrap.py
```

Details: [cms/CMS_LOCK.md](cms/CMS_LOCK.md).

---

## Asset rules that keep the page fast

- Photos and short audio can be inlined or loaded from the Higgsfield CDN.
- Video is always a hosted file. Never base64 — it inflates about 33% and blocks first paint.
- The hero background video is silent on purpose (audio stripped).
- `og:image` must be an absolute `https://` URL. Crawlers fetch it from their own servers, so a data URI produces no share card.
- Current share image: `https://upload.higgsfield.ai/user_36SLpLHo0MVI10STslhM0wOZWEK/2244481a-643d-4139-b03b-ec907f39fadb.jpg`

---

## Credits

- Artist: [Icewear Vezzo](https://www.instagram.com/icewear_vezzo)
- Label: Iced Up Records
- Campaign partner: Foundation Media
- Site + campaign infrastructure: [Digital Currensy Inc.](https://github.com/DigitalCurrensy)
- Playable game host: [Higgsfield](https://blue-cloud-787.higgsfield.gg/)

Icewear Vezzo name, likeness, music, artwork, and ROP 4 marks remain the property of the artist and partners. See [LICENSE](LICENSE).
