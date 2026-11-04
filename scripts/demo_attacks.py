"""Zero-trust attack simulation.

Scenarios, each expected to be REJECTED by the verifier:

  1. Happy path (sanity check — must ACCEPT)
  2. Replay of the same envelope
  3. Tampered recommendation (proposed_value changed)
  4. Unapproved model version (signed correctly but version not on allowlist)
  5. Stale timestamp (issued 10 minutes ago, skew limit 5 minutes)
  6. Forged signature (wrong agent key)
"""

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "zero-trust"))

from signing.signer import AdvisorySigner  # noqa: E402
from verifier.verifier import verify_envelope  # noqa: E402
from verifier.nonce_store import NonceStore  # noqa: E402

APPROVED_MODEL = {
    "version": "0.1.0",
    "artifact_hash": "sha256:" + "b" * 64,
    "training_run": "run-2026-11-04-001",
}


def _base_payload(model: dict | None = None, issued_at: str | None = None) -> dict:
    p = {
        "model": model or APPROVED_MODEL,
        "unit": "bleaching",
        "recommendation": {
            "variable": "earth_dose_kg_per_t",
            "current_value": 8.0,
            "proposed_value": 16.9,
            "confidence": 0.82,
        },
        "constraints": {"within_bounds": True, "quality_preserved": True, "violations": []},
        "provenance": {
            "input_window": "2026-11-04T08:00:00Z/PT1H",
            "model_card_ref": "model-card-bleaching-v0.1.0",
        },
        "evidence_ref": "EVID-DEMO",
    }
    if issued_at is not None:
        p["issued_at"] = issued_at
    return p


def _show(label: str, result: dict) -> None:
    print(f"\n--- {label} ---")
    print(f"  ok:     {result['ok']}")
    print(f"  stage:  {result['stage']}")
    print(f"  reason: {result['reason']}")


def main() -> int:
    signer = AdvisorySigner("quality")

    # 1. Happy path
    store = NonceStore()
    env = signer.sign_envelope(_base_payload())
    r = verify_envelope(env, nonce_store=store)
    _show("1. Happy path (expect ACCEPT)", r)
    assert r["ok"] is True

    # 2. Replay
    r = verify_envelope(env, nonce_store=store)
    _show("2. Replay of same envelope (expect REJECT)", r)
    assert r["ok"] is False and r["stage"] == "nonce"

    # 3. Tampered
    store = NonceStore()
    tampered = json.loads(json.dumps(signer.sign_envelope(_base_payload())))
    tampered["recommendation"]["proposed_value"] = 999.0
    r = verify_envelope(tampered, nonce_store=store)
    _show("3. Tampered recommendation (expect REJECT)", r)
    assert r["ok"] is False and r["stage"] == "signature"

    # 4. Unapproved model version, correctly signed
    store = NonceStore()
    rogue_model = {
        "version": "0.9.9",
        "artifact_hash": "sha256:" + "c" * 64,
        "training_run": "unapproved-run",
    }
    env = signer.sign_envelope(_base_payload(model=rogue_model))
    r = verify_envelope(env, nonce_store=store)
    _show("4. Unapproved model version (expect REJECT)", r)
    assert r["ok"] is False and r["stage"] == "policy"

    # 5. Stale timestamp
    store = NonceStore()
    stale = (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat()
    env = signer.sign_envelope(_base_payload(issued_at=stale))
    r = verify_envelope(env, nonce_store=store, max_skew_seconds=300)
    _show("5. Stale timestamp (expect REJECT)", r)
    assert r["ok"] is False and r["stage"] == "freshness"

    # 6. Forged signature: signed by maintenance, key_id claim swapped to quality
    store = NonceStore()
    env = signer.sign_envelope(_base_payload())
    env["signature"]["key_id"] = "maintenance-v1"
    r = verify_envelope(env, nonce_store=store)
    _show("6. Forged signature (key_id tamper, expect REJECT)", r)
    assert r["ok"] is False

    print("\nOK: 5 attacks rejected, 1 happy path accepted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
