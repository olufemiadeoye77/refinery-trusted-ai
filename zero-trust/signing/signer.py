"""Signs advisory envelopes with an agent's Ed25519 private key."""

import base64
import json
from datetime import datetime, timezone
from uuid import uuid4

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .keys import AGENTS, ensure_keypair


def _canonical(payload: dict) -> bytes:
    """Deterministic JSON of everything except the signature block."""
    body = {k: v for k, v in payload.items() if k != "signature"}
    return json.dumps(body, sort_keys=True, separators=(",", ":")).encode()


class AdvisorySigner:
    def __init__(self, agent: str):
        if agent not in AGENTS:
            raise ValueError(f"unknown agent: {agent}")
        self.agent = agent
        priv_path, _ = ensure_keypair(agent)
        self._key = Ed25519PrivateKey.from_private_bytes(priv_path.read_bytes())

    def sign_envelope(self, payload: dict) -> dict:
        if "signature" in payload:
            raise ValueError("payload is already signed")
        signed = dict(payload)
        signed.setdefault("envelope_id", str(uuid4()))
        signed.setdefault("issued_at", datetime.now(timezone.utc).isoformat())
        signed.setdefault("nonce", uuid4().hex)
        signed.setdefault("agent", self.agent)
        sig = self._key.sign(_canonical(signed))
        signed["signature"] = {
            "alg": "Ed25519",
            "key_id": f"{self.agent}-v1",
            "value": base64.b64encode(sig).decode(),
        }
        return signed
