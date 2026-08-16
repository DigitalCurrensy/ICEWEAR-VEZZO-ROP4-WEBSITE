#!/usr/bin/env python3
"""
ICEWEAR — Payload CMS wrap (MIT house lock) — The Drop

Smallest wrap that makes draft → named-human stamp → publish real.

Law:
  - Payload MIT only. No Tina. No second CMS.
  - Bind 127.0.0.1 / localhost. Fail closed if URL/token missing.
  - Icewear-only collection: drops. Not SMITH, spa, NIL, or Hub.
  - Agents draft. A named human must stamp before a drop goes live.
  - Guard wrap stays in Guard. Game stays a game.

Usage:
    python3 cms/payload_wrap.py --draft cms/fixtures/the-drop.draft.json
    python3 cms/payload_wrap.py --approve SLUG --actor-name YOU
    python3 cms/payload_wrap.py --publish SLUG --actor-name YOU
    python3 cms/payload_wrap.py --emit
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
QUEUE_DEFAULT = HERE / "queue" / "drops.json"
LIVE_DEFAULT = HERE / "out" / "drops.json"

if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from law import (  # noqa: E402
    AGENT,
    ALLOWED_PRODUCTS,
    DROPS_COLLECTION,
    FORBIDDEN_PRODUCTS,
    GAME_HOST,
    HUMAN,
    ICEWEAR_CMS_LAW,
    SITE_FILES,
)

LOCAL_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})
Transport = Callable[[str, str, dict[str, Any] | None], dict[str, Any]]


class PayloadUnconfigured(RuntimeError):
    """PAYLOAD_URL / PAYLOAD_TOKEN missing — fail closed, no silent CMS."""


class PayloadBindError(RuntimeError):
    """Payload is not local, or this wrap was pointed at another product."""


class HitlRequired(RuntimeError):
    """Approve and publish are human-only and need a named stamp."""


class IllegalTransition(RuntimeError):
    """Status machine refused the move (draft cannot publish itself)."""


class GameStaysGame(RuntimeError):
    """The Drop seat must not write the playable game or site chrome."""


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _token_from_env() -> str:
    return (
        os.environ.get("PAYLOAD_TOKEN", "").strip()
        or os.environ.get("PAYLOAD_SECRET", "").strip()
    )


def require_payload(
    url: str | None = None,
    token: str | None = None,
    product: str | None = None,
) -> tuple[str, str]:
    """Fail closed unless a local Payload seat is configured for Icewear."""
    raw_product = (
        product
        if product is not None
        else os.environ.get("ICEWEAR_PRODUCT", "icewear")
    )
    product = str(raw_product or "").strip() or "icewear"
    if product.lower() in FORBIDDEN_PRODUCTS:
        raise PayloadBindError(
            "Icewear The Drop only — do not mount this wrap on SMITH, spa, NIL, or Hub"
        )
    if product.lower() not in ALLOWED_PRODUCTS:
        raise PayloadBindError(
            f"Icewear The Drop only — unknown product {product!r}"
        )
    url = (url if url is not None else os.environ.get("PAYLOAD_URL", "")).strip()
    token = (token if token is not None else _token_from_env()).strip()
    if not url or not token:
        raise PayloadUnconfigured(
            "PAYLOAD_URL and PAYLOAD_TOKEN required; fail closed (no silent CMS)"
        )
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if host == "0.0.0.0" or parsed.hostname == "0.0.0.0":
        raise PayloadBindError("Payload must not bind 0.0.0.0")
    if host not in LOCAL_HOSTS:
        raise PayloadBindError(f"Payload must bind 127.0.0.1 (got {host or url!r})")
    if parsed.scheme not in {"http", "https"}:
        raise PayloadBindError(f"Payload URL scheme must be http(s), got {parsed.scheme!r}")
    return url.rstrip("/"), token


def _slugify(title: str) -> str:
    raw = "".join(ch.lower() if ch.isalnum() else "-" for ch in title).strip("-")
    while "--" in raw:
        raw = raw.replace("--", "-")
    return raw[:72] or "untitled"


def _require_named_human(actor_role: str, actor_name: str, verb: str) -> str:
    if actor_role != HUMAN:
        raise HitlRequired(f"{verb} is human-only — agents draft only")
    name = str(actor_name or "").strip()
    if not name:
        raise HitlRequired(f"{verb} requires a named human stamp")
    if name.lower() in {AGENT, "bot", "cursor", "auto"}:
        raise HitlRequired(f"{verb} requires a named human — {name!r} is not a human stamp")
    return name


def _guard_site_path(path: Path) -> Path:
    resolved = path.resolve()
    name = resolved.name
    if name in SITE_FILES:
        raise GameStaysGame(f"refusing to write {name} — game stays a game")
    text = str(resolved)
    if GAME_HOST.replace(".", "_") in text or "/index.html" in text:
        raise GameStaysGame("refusing to write the playable game surface")
    return path


def _http_transport(base_url: str, token: str) -> Transport:
    def call(method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(
            f"{base_url}{path}",
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                raw = resp.read().decode()
        except urllib.error.URLError as exc:
            raise PayloadUnconfigured(
                f"Payload unreachable at {base_url} — fail closed ({exc})"
            ) from exc
        return json.loads(raw) if raw else {}

    return call


class DropStore:
    """Local HITL queue. Not a second CMS — Payload remains the lock."""

    def __init__(self, path: Path) -> None:
        self.path = _guard_site_path(path)

    def _empty(self) -> dict[str, Any]:
        return {
            "product": "icewear",
            "cms": "payload-mit",
            "seat": "the-drop",
            "law": ICEWEAR_CMS_LAW,
            "drops": [],
        }

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return self._empty()
        data = json.loads(self.path.read_text())
        if not isinstance(data, dict):
            raise IllegalTransition("drop queue is corrupt")
        data.setdefault("drops", [])
        return data

    def save(self, data: dict[str, Any]) -> None:
        _guard_site_path(self.path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    def all(self) -> list[dict[str, Any]]:
        return list(self.load().get("drops") or [])

    def get(self, slug: str) -> dict[str, Any]:
        for drop in self.all():
            if drop.get("slug") == slug:
                return dict(drop)
        raise IllegalTransition(f"unknown slug {slug!r}")

    def upsert(self, drop: dict[str, Any]) -> dict[str, Any]:
        data = self.load()
        rows = [d for d in data.get("drops") or [] if d.get("slug") != drop["slug"]]
        rows.append(drop)
        data["drops"] = rows
        data["updated_at"] = _now()
        self.save(data)
        return dict(drop)


def emit_live_surface(
    store: DropStore,
    live_out: Path | str = LIVE_DEFAULT,
) -> dict[str, Any]:
    """Write live drops only. Drafts stay off the public surface."""
    out = _guard_site_path(Path(live_out))
    live = [d for d in store.all() if d.get("status") == "live"]
    public = {
        "brand": "ICEWEAR VEZZO",
        "product": "icewear",
        "seat": "the-drop",
        "cms": "payload-mit",
        "generated_at": _now(),
        "hitl": "agents draft · named human stamps · human publishes",
        "game": GAME_HOST,
        "game_stays_game": True,
        "drops": [
            {
                "slug": d["slug"],
                "title": d["title"],
                "dek": d.get("dek") or "",
                "published_by": d.get("published_by"),
                "published_at": d.get("published_at"),
            }
            for d in live
        ],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(public, indent=2, ensure_ascii=False) + "\n")
    return public


class PayloadWrap:
    """Local Payload client + HITL state machine for Icewear drops."""

    def __init__(
        self,
        url: str | None = None,
        token: str | None = None,
        secret: str | None = None,
        product: str | None = None,
        transport: Transport | None = None,
        queue_path: Path | str | None = None,
        live_out: Path | str | None = None,
        collection: str = DROPS_COLLECTION,
    ) -> None:
        self.url, self.token = require_payload(url, token if token is not None else secret, product)
        if collection != DROPS_COLLECTION:
            raise PayloadBindError(
                f"Icewear-only collection: {DROPS_COLLECTION!r} (got {collection!r})"
            )
        self.collection = collection
        self.store = DropStore(Path(queue_path) if queue_path else QUEUE_DEFAULT)
        self.live_out = Path(live_out) if live_out else LIVE_DEFAULT
        self.transport = transport or _http_transport(self.url, self.token)

    def draft(self, entry: dict[str, Any], actor_role: str = AGENT) -> dict[str, Any]:
        """Create a draft. Never live. Agents may draft; they may not publish."""
        if actor_role not in {AGENT, HUMAN}:
            raise HitlRequired(f"unknown actor_role {actor_role!r}")
        title = str(entry.get("title") or "").strip()
        if not title:
            raise IllegalTransition("draft requires a title")
        slug = str(entry.get("slug") or _slugify(title))
        if entry.get("status") in {"live", "approved", "published"}:
            raise IllegalTransition("draft cannot publish itself")
        payload = {
            "slug": slug,
            "title": title,
            "dek": str(entry.get("dek") or ""),
            "body": str(entry.get("body") or ""),
            "status": "draft",
            "_status": "draft",
            "agent": str(entry.get("agent") or "CONTENT-GEN-02"),
            "product": "icewear",
            "seat": "the-drop",
            "license": "payload-mit",
            "game_stays_game": True,
            "approved_by": None,
            "approved_at": None,
            "published_by": None,
            "published_at": None,
        }
        remote = self.transport("POST", f"/api/{self.collection}", payload)
        payload["payload_id"] = str(remote.get("id") or remote.get("doc", {}).get("id") or "")
        return self.store.upsert(payload)

    def approve(self, slug: str, actor_role: str, actor_name: str = "") -> dict[str, Any]:
        name = _require_named_human(actor_role, actor_name, "approve")
        drop = self.store.get(slug)
        if drop["status"] == "live":
            raise IllegalTransition("already live")
        if drop["status"] != "draft":
            raise IllegalTransition(f"approve only from draft (got {drop['status']})")
        stamp = _now()
        remote_id = drop.get("payload_id") or slug
        self.transport(
            "PATCH",
            f"/api/{self.collection}/{remote_id}",
            {
                "status": "approved",
                "_status": "draft",
                "approved_by": name,
                "approved_at": stamp,
            },
        )
        drop["status"] = "approved"
        drop["approved_by"] = name
        drop["approved_at"] = stamp
        return self.store.upsert(drop)

    def publish(self, slug: str, actor_role: str, actor_name: str = "") -> dict[str, Any]:
        name = _require_named_human(actor_role, actor_name, "publish")
        drop = self.store.get(slug)
        if drop["status"] == "draft":
            raise IllegalTransition("draft cannot publish itself — a named human must stamp first")
        if drop["status"] != "approved":
            raise IllegalTransition(f"publish only from approved (got {drop['status']})")
        if not str(drop.get("approved_by") or "").strip():
            raise HitlRequired("publish requires a named human stamp on the drop")
        stamp = _now()
        remote_id = drop.get("payload_id") or slug
        self.transport(
            "PATCH",
            f"/api/{self.collection}/{remote_id}",
            {
                "status": "live",
                "_status": "published",
                "published_by": name,
                "published_at": stamp,
            },
        )
        drop["status"] = "live"
        drop["published_by"] = name
        drop["published_at"] = stamp
        saved = self.store.upsert(drop)
        emit_live_surface(self.store, self.live_out)
        return saved


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Icewear Payload wrap — The Drop draft/approve/publish")
    ap.add_argument("--draft", metavar="JSON", help="path to entry.draft.json")
    ap.add_argument("--approve", metavar="SLUG")
    ap.add_argument("--publish", metavar="SLUG")
    ap.add_argument("--actor-name", default="")
    ap.add_argument("--emit", action="store_true", help="rewrite live drops.json")
    ap.add_argument("--queue", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args(argv)

    queue = args.queue or QUEUE_DEFAULT
    live_out = args.out or LIVE_DEFAULT

    if args.emit and not (args.draft or args.approve or args.publish):
        public = emit_live_surface(DropStore(queue), live_out)
        print(f"emitted {len(public['drops'])} live drop(s) → {Path(live_out).name}")
        return 0

    wrap = PayloadWrap(queue_path=queue, live_out=live_out)
    if args.draft:
        entry = json.loads(Path(args.draft).read_text())
        drop = wrap.draft(entry, actor_role=AGENT)
        print(f"drafted {drop['slug']} status={drop['status']}")
    if args.approve:
        drop = wrap.approve(args.approve, actor_role=HUMAN, actor_name=args.actor_name)
        print(f"approved {drop['slug']} by {drop['approved_by']}")
    if args.publish:
        drop = wrap.publish(args.publish, actor_role=HUMAN, actor_name=args.actor_name)
        print(f"published {drop['slug']} by {drop['published_by']} (HITL)")
    if args.emit or args.publish:
        emit_live_surface(wrap.store, wrap.live_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
