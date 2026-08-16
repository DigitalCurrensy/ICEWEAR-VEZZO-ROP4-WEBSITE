# CMS lock — ICEWEAR The Drop only

Payload **MIT** is the house CMS. This repo wraps it for **one** collection:
`drops` → The Drop. Tina is not started. A second CMS is not invented.

## Seat

- Product: `icewear`
- Seat: `the-drop`
- Bind: `127.0.0.1` / `localhost` (`PAYLOAD_URL` + `PAYLOAD_TOKEN`)
- Fail closed if URL or token is missing — no silent publish, no fake CMS success
- Not SMITH. Not spa. Not NIL. Not Hub. Do not vendor Payload here.
- Guard wrap stays in Guard. This seat does not absorb it.

## HITL

1. Agent (or human) **drafts**. Status stays `draft`. Draft cannot publish itself.
2. A **named human** stamps approve (`--actor-name` required).
3. A **named human** publishes. Only then does the row go `live`.

Agent never self-publishes.

## Game stays a game

The ROP 4 night run (`blue-cloud-787.higgsfield.gg`) stays a playable game.
This wrap does not write `index.html` or `build.sh`. Existing content guards stay.

## CLI

```bash
# requires PAYLOAD_URL=http://127.0.0.1:3000 and PAYLOAD_TOKEN
python3 cms/payload_wrap.py --draft cms/fixtures/the-drop.draft.json
python3 cms/payload_wrap.py --approve the-drop --actor-name YOU
python3 cms/payload_wrap.py --publish the-drop --actor-name YOU
python3 cms/tests/test_payload_wrap.py
```

Live keys stay out of git. Use `.env` locally; `.env.example` is placeholders only.
