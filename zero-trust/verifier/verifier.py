"""Zero-trust enforcement point for advisory envelopes.

Verification order (fail-closed at every step):

  1. schema presence (signature block exists, alg is Ed25519)
  2. key registry: key_id maps to a known agent, agent claim matches key
  3. signature validity against the agent's public key
  4. model authorization: version AND artifact hash on the allowlist
  5. timestamp freshness within skew window
  6. nonce not previously seen (replay protection)

Any failure returns ok=False with a reason. Callers must refuse the
advisory on ok=False.
"""

import base64
import json
from datetime import datetime, timezone

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from signing.keys import AGENTS, KEYS_DIR
from verifier.nonce_store import NonceStore
from policy.checker import model_approved


def _canonical(payload: dict) -> bytes:
    body = {k: v for k, v in payload.items() if k != "signature"}
    return json.dumps(body, sort_keys=True, separators=(",", ":")).encode()


_DEFAULT_STORE = NonceStore()


def verify_envelope(
    payload: dict,
    *,
    nonce_store: NonceStore | None = None,
    max_skew_seconds: int = 300,
    check_policy: bool = True,
    check_freshness: bool = True,
) -> dict:
    store = nonce_store if nonce_store is not None else _DEFAULT_STORE

    # 1. signature block
    sig_block = payload.get("signature") or {}
    if not sig_block:
        return {"ok": False, "stage": "signature_present", "reason": "missing signature", "agent": None}
    if sig_block.get("alg") != "Ed25519":
        return {"ok": False, "stage": "signature_alg", "reason": f"unsupported alg: {sig_block.get('alg')}", "agent": None}

    # 2. key registry
    key_id = sig_block.get("key_id", "")
    if not key_id.endswith("-v1"):
        return {"ok": False, "stage": "key_registry", "reason": f"bad key_id format: {key_id}", "agent": None}
    agent = key_id[:-3]
    if agent not in AGENTS:
        return {"ok": False, "stage": "key_registry", "reason": f"unknown agent: {agent}", "agent": None}
    if payload.get("agent") != agent:
        return {"ok": False, "stage": "agent_match", "reason": f"agent mismatch: header={payload.get('agent')} key={agent}", "agent": agent}

    # 3. signature
    pub_path = KEYS_DIR / f"{agent}.pub"
    if not pub_path.exists():
        return {"ok": False, "stage": "signature", "reason": f"no public key for {agent}", "agent": agent}
    pub = Ed25519PublicKey.from_public_bytes(pub_path.read_bytes())
    try:
        pub.verify(base64.b64decode(sig_block["value"]), _canonical(payload))
    except Exception as e:
        return {"ok": False, "stage": "signature", "reason": f"signature invalid: {e}", "agent": agent}

    # 4. model authorization
    if check_policy:
        pol = model_approved(payload.get("model", {}))
        if not pol["allow"]:
            return {"ok": False, "stage": "policy", "reason": pol["reason"], "agent": agent}

    # 5. freshness
    if check_freshness:
        issued_at = payload.get("issued_at")
        if not issued_at:
            return {"ok": False, "stage": "freshness", "reason": "missing issued_at", "agent": agent}
        try:
            issued = datetime.fromisoformat(issued_at.replace("Z", "+00:00"))
            if issued.tzinfo is None:
                issued = issued.replace(tzinfo=timezone.utc)
        except ValueError as e:
            return {"ok": False, "stage": "freshness", "reason": f"bad issued_at: {e}", "agent": agent}
        skew = abs((datetime.now(timezone.utc) - issued).total_seconds())
        if skew > max_skew_seconds:
            return {"ok": False, "stage": "freshness", "reason": f"skew {skew:.0f}s exceeds {max_skew_seconds}s", "agent": agent}

    # 6. replay protection
    nonce = payload.get("nonce")
    if not nonce:
        return {"ok": False, "stage": "nonce", "reason": "missing nonce", "agent": agent}
    if store.seen(nonce):
        return {"ok": False, "stage": "nonce", "reason": f"nonce already seen: {nonce[:16]}...", "agent": agent}
    store.record(nonce)

    return {"ok": True, "stage": "ok", "reason": "ok", "agent": agent}
