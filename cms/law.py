"""Icewear The Drop — Payload MIT law.

Guard wrap stays in Guard. This seat does not absorb SMITH, spa, NIL, or Hub.
Game stays a game. Agents draft. A named human stamps before a drop goes live.
"""

from __future__ import annotations

from typing import Final

HUMAN: Final = "human"
AGENT: Final = "agent"

ICEWEAR_CMS_LAW = {
    "houseCms": "payload-mit",
    "product": "icewear",
    "seat": "the-drop",
    "collection": "drops",
    "tina": "never-start",
    "agents": "draft-only",
    "publish": "human-only",
    "namedStamp": True,
    "game": "stays-a-game",
    "guardWrap": "keep-in-guard-do-not-absorb",
    "absorb": {
        "smith": False,
        "spa": False,
        "nil": False,
        "hub": False,
        "guard": False,
    },
}

FORBIDDEN_PRODUCTS = frozenset(
    {
        "smith",
        "spa",
        "nil",
        "hub",
        "nil-mixtape",
        "the-hub",
        "the hub",
        "agent-health-spa",
        "smith_estates_ltd",
        "sagitarius",
        "sagittarius",
        "tmwy",
    }
)

ALLOWED_PRODUCTS = frozenset({"icewear", "icewear-vezzo", "rop4", "the-drop"})
DROPS_COLLECTION = "drops"
GAME_HOST = "blue-cloud-787.higgsfield.gg"
SITE_FILES = frozenset({"index.html", "build.sh"})


def assert_agent_draft_only(action: str) -> None:
    if action != "draft":
        raise PermissionError(
            "Icewear law: agents draft. A named human stamps before a drop goes live."
        )


def can_stamp_live(actor: str, actor_name: str) -> bool:
    return actor == HUMAN and bool(str(actor_name or "").strip())
