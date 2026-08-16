#!/usr/bin/env python3
"""HITL + fail-closed tests for the Icewear The Drop Payload wrap."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

CMS = Path(__file__).resolve().parents[1]
ROOT = CMS.parent
if str(CMS) not in sys.path:
    sys.path.insert(0, str(CMS))

from law import GAME_HOST, ICEWEAR_CMS_LAW, can_stamp_live  # noqa: E402
from payload_wrap import (  # noqa: E402
    GameStaysGame,
    HitlRequired,
    IllegalTransition,
    PayloadBindError,
    PayloadUnconfigured,
    PayloadWrap,
    emit_live_surface,
    require_payload,
)


def _memory_transport() -> tuple[list[tuple], callable]:
    calls: list[tuple] = []
    seq = {"n": 0}

    def call(method: str, path: str, body: dict | None = None) -> dict:
        seq["n"] += 1
        calls.append((method, path, body))
        return {"id": f"doc-{seq['n']}", "doc": {"id": f"doc-{seq['n']}"}}

    return calls, call


def _wrap(queue: Path) -> tuple[PayloadWrap, list]:
    calls, transport = _memory_transport()
    wrap = PayloadWrap(
        url="http://127.0.0.1:3000",
        token="test-token",
        product="icewear",
        transport=transport,
        queue_path=queue,
        live_out=queue.parent / "drops.live.json",
    )
    return wrap, calls


ENTRY = {
    "slug": "the-drop",
    "title": "The Drop — ROP 4",
    "dek": "Draft only until a named human stamps.",
    "body": "Payload MIT. Game stays a game.",
    "agent": "CONTENT-GEN-02",
}


class FailClosedTests(unittest.TestCase):
    def test_unconfigured_payload_fails_closed(self) -> None:
        env = os.environ.copy()
        try:
            os.environ.pop("PAYLOAD_URL", None)
            os.environ.pop("PAYLOAD_TOKEN", None)
            os.environ.pop("PAYLOAD_SECRET", None)
            os.environ.pop("ICEWEAR_PRODUCT", None)
            with self.assertRaises(PayloadUnconfigured):
                require_payload("", "")
            with self.assertRaises(PayloadUnconfigured):
                require_payload(None, None)
            with self.assertRaises(PayloadUnconfigured):
                PayloadWrap(url="", token="")
            with self.assertRaises(PayloadUnconfigured):
                PayloadWrap(url="http://127.0.0.1:3000", token="")
            with self.assertRaises(PayloadUnconfigured):
                PayloadWrap()
        finally:
            os.environ.clear()
            os.environ.update(env)

    def test_token_alias_secret_is_accepted(self) -> None:
        env = os.environ.copy()
        try:
            os.environ.pop("PAYLOAD_TOKEN", None)
            os.environ["PAYLOAD_URL"] = "http://127.0.0.1:3000"
            os.environ["PAYLOAD_SECRET"] = "alias-only"
            url, token = require_payload()
            self.assertEqual(url, "http://127.0.0.1:3000")
            self.assertEqual(token, "alias-only")
        finally:
            os.environ.clear()
            os.environ.update(env)

    def test_non_local_bind_fails_closed(self) -> None:
        with self.assertRaises(PayloadBindError):
            require_payload("https://cms.example.com", "token")
        with self.assertRaises(PayloadBindError):
            require_payload("http://0.0.0.0:3000", "token")

    def test_foreign_product_fails_closed(self) -> None:
        for product in ("SMITH", "spa", "NIL", "Hub", "nil-mixtape"):
            with self.assertRaises(PayloadBindError):
                require_payload(
                    "http://127.0.0.1:3000", "token", product=product
                )


class HitlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.queue = Path(self.tmp.name) / "drops.json"
        self.wrap, self.calls = _wrap(self.queue)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_draft_cannot_publish_itself(self) -> None:
        drop = self.wrap.draft(ENTRY, actor_role="agent")
        self.assertEqual(drop["status"], "draft")
        self.assertIsNone(drop.get("published_at"))
        with self.assertRaises(IllegalTransition):
            self.wrap.draft({**ENTRY, "status": "live"}, actor_role="agent")
        with self.assertRaises(IllegalTransition):
            self.wrap.publish(drop["slug"], actor_role="human", actor_name="swish")
        queued = json.loads(self.queue.read_text())["drops"]
        self.assertEqual(queued[0]["status"], "draft")
        public = emit_live_surface(self.wrap.store, self.wrap.live_out)
        self.assertEqual(public["drops"], [])

    def test_named_human_must_stamp_before_live(self) -> None:
        drop = self.wrap.draft(ENTRY, actor_role="agent")
        with self.assertRaises(HitlRequired):
            self.wrap.approve(drop["slug"], actor_role="agent", actor_name="bot")
        with self.assertRaises(HitlRequired):
            self.wrap.approve(drop["slug"], actor_role="human", actor_name="")
        with self.assertRaises(HitlRequired):
            self.wrap.approve(drop["slug"], actor_role="human", actor_name="cursor")
        with self.assertRaises(IllegalTransition):
            self.wrap.publish(drop["slug"], actor_role="human", actor_name="swish")
        approved = self.wrap.approve(
            drop["slug"], actor_role="human", actor_name="swish"
        )
        self.assertEqual(approved["status"], "approved")
        self.assertEqual(approved["approved_by"], "swish")
        self.assertFalse(can_stamp_live("agent", "bot"))
        with self.assertRaises(HitlRequired):
            self.wrap.publish(drop["slug"], actor_role="agent", actor_name="bot")
        live = self.wrap.publish(
            drop["slug"], actor_role="human", actor_name="swish"
        )
        self.assertEqual(live["status"], "live")
        self.assertEqual(live["published_by"], "swish")
        self.assertTrue(live["published_at"])
        public = json.loads(self.wrap.live_out.read_text())
        self.assertEqual(len(public["drops"]), 1)
        self.assertEqual(public["drops"][0]["slug"], drop["slug"])
        self.assertTrue(public["game_stays_game"])

    def test_live_surface_omits_drafts(self) -> None:
        self.wrap.draft(ENTRY, actor_role="agent")
        public = emit_live_surface(self.wrap.store, self.wrap.live_out)
        self.assertEqual(public["drops"], [])
        queued = json.loads(self.queue.read_text())["drops"]
        self.assertEqual(len(queued), 1)
        self.assertEqual(queued[0]["status"], "draft")


class GameAndLockTests(unittest.TestCase):
    def test_game_stays_a_game(self) -> None:
        site = (ROOT / "index.html").read_text()
        self.assertIn(GAME_HOST, site)
        self.assertIn('id="game"', site)
        build = (ROOT / "build.sh").read_text()
        self.assertIn("blue-cloud-787", build)
        self.assertIn("guards passed", build)

    def test_refuses_to_write_site_or_game(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wrap, _ = _wrap(Path(tmp) / "drops.json")
            with self.assertRaises(GameStaysGame):
                emit_live_surface(wrap.store, ROOT / "index.html")
            with self.assertRaises(GameStaysGame):
                emit_live_surface(wrap.store, ROOT / "build.sh")

    def test_no_second_cms_and_no_tina(self) -> None:
        self.assertEqual(ICEWEAR_CMS_LAW["houseCms"], "payload-mit")
        self.assertEqual(ICEWEAR_CMS_LAW["tina"], "never-start")
        self.assertFalse(ICEWEAR_CMS_LAW["absorb"]["smith"])
        self.assertFalse(ICEWEAR_CMS_LAW["absorb"]["spa"])
        self.assertFalse(ICEWEAR_CMS_LAW["absorb"]["nil"])
        self.assertFalse(ICEWEAR_CMS_LAW["absorb"]["hub"])
        self.assertFalse(ICEWEAR_CMS_LAW["absorb"]["guard"])
        self.assertFalse((ROOT / "tina").exists())
        self.assertFalse((ROOT / ".tina").exists())
        self.assertFalse(any(ROOT.glob("**/tina-config.*")))

    def test_no_live_keys_in_git(self) -> None:
        example = (ROOT / ".env.example").read_text()
        self.assertIn("PAYLOAD_URL=", example)
        self.assertIn("PAYLOAD_TOKEN=", example)
        self.assertNotIn("sk_live", example)
        ignore = (ROOT / ".gitignore").read_text()
        self.assertIn(".env", ignore)
        self.assertIn("!.env.example", ignore)


if __name__ == "__main__":
    unittest.main()
