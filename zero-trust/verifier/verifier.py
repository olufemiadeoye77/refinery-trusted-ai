"""Verifies signed advisory envelopes against the key registry."""

import base64
import json

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from signing.keys import AGENTS, KEYS_DIR


def _canonical(payload: dict) -> bytes:
    body = {k: v for k, v in payload.items() if k != "signature"}
    return json.dumps(body, sort_keys=True, separators=(",", ":")).encode()


def verify_envelope(payload: dict) -> dict:
    """Return {'ok': bool, 'reason': str, 'agent': str|None}. Fail-closed."""
    sig_block = payload.get("signature") or {}
    if not sig_block:
        return {"ok": False, "reason": "missing signature", "agent": None}
    if sig_block.get("alg") != "Ed25519":
        return {"ok": False, "reason": f"unsupported alg: {sig_block.get('alg')}", "agent": None}
    key_id = sig_block.get("key_id", "")
    if not key_id.endswith("-v1"):
        return {"ok": False, "reason": f"unknown key_id format: {key_id}", "agent": None}
    agent = key_id[:-3]
    if agent not in AGENTS:
        return {"ok": False, "reason": f"unknown agent: {agent}", "agent": None}
    if payload.get("agent") != agent:
        return {"ok": False, "reason": f"agent mismatch: header={payload.get('agent')} key={agent}", "agent": agent}

    pub_path = KEYS_DIR / f"{agent}.pub"
    if not pub_path.exists():
        return {"ok": False, "reason": f"no public key for {agent}", "agent": agent}
    pub = Ed25519PublicKey.from_public_bytes(pub_path.read_bytes())

    try:
        sig = base64.b64decode(sig_block["value"])
        pub.verify(sig, _canonical(payload))
    except Exception as e:
        return {"ok": False, "reason": f"signature invalid: {e}", "agent": agent}

    return {"ok": True, "reason": "ok", "agent": agent}
