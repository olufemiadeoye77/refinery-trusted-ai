"""Signing round-trip demo: sign a bleaching advisory, verify, then tamper-test."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "zero-trust"))

from signing.signer import AdvisorySigner  # noqa: E402
from verifier.verifier import verify_envelope  # noqa: E402


def main() -> int:
    payload = {
        "model": {
            "version": "0.1.0",
            "artifact_hash": "sha256:" + "b" * 64,
            "training_run": "run-2026-11-04-001",
        },
        "unit": "bleaching",
        "recommendation": {
            "variable": "earth_dose_kg_per_t",
            "current_value": 8.0,
            "proposed_value": 14.5,
            "confidence": 0.87,
        },
        "constraints": {
            "within_bounds": True,
            "quality_preserved": True,
            "violations": [],
        },
        "provenance": {
            "input_window": "2026-11-04T08:00:00Z/PT1H",
            "model_card_ref": "model-card-bleaching-v0.1.0",
        },
        "evidence_ref": "EVID-0001",
    }

    signed = AdvisorySigner("quality").sign_envelope(payload)
    print("=== SIGNED ENVELOPE ===")
    print(json.dumps(signed, indent=2))

    good = verify_envelope(signed)
    print("\n=== VERIFY (untampered) ===")
    print(good)
    assert good["ok"] is True

    tampered = json.loads(json.dumps(signed))
    tampered["recommendation"]["proposed_value"] = 999.0
    bad = verify_envelope(tampered)
    print("\n=== VERIFY (tampered proposed_value) ===")
    print(bad)
    assert bad["ok"] is False

    print("\nOK: sign -> verify -> tamper-detect all behaved correctly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
