"""Icewear Payload path forward — The Drop seat.

Do not mount admin or connect a database from this file until a human sets
PAYLOAD_URL and PAYLOAD_TOKEN. Do not start Tina. Do not vendor Payload.
Guard wrap stays in Guard. Game stays a game.
"""

from __future__ import annotations

from law import DROPS_COLLECTION, ICEWEAR_CMS_LAW

icewear_payload_config = {
    "secretFromEnv": "PAYLOAD_TOKEN",
    "secretAliasFromEnv": "PAYLOAD_SECRET",
    "urlFromEnv": "PAYLOAD_URL",
    "adminMounted": False,
    "collections": [DROPS_COLLECTION],
    "law": ICEWEAR_CMS_LAW,
    "bind": "127.0.0.1",
    "product": "icewear",
    "seat": "the-drop",
}

ICEWEAR_COLLECTION_SLUGS = (DROPS_COLLECTION,)
