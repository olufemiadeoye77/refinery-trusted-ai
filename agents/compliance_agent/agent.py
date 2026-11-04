"""Compliance agent: binds a proposal to an evidence record before it is
signed. Produces an evidence_ref that the orchestrator embeds in the
signed envelope. Evidence files live in compliance/evidence/ (gitignored)."""

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

EVIDENCE_DIR = Path("compliance/evidence")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


def attest(proposal: dict, model: dict, input_window: str) -> str:
    evidence_id = f"EVID-{uuid4().hex[:12].upper()}"
    record = {
        "evidence_id": evidence_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "proposal": proposal,
        "input_window": input_window,
        "controls": ["A.6.2.6", "A.9.2", "CL.9.1"],
        "decision": "pending_human_approval",
    }
    (EVIDENCE_DIR / f"{evidence_id}.json").write_text(json.dumps(record, indent=2))
    return evidence_id
