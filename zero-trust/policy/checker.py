"""Python implementation of model-allowlist.rego.

Kept in lock-step with the Rego source. CI runs this; the Rego file is
the human-readable policy of record and can be tested with `opa test`
or `opa eval` in environments where OPA is installed.
"""

import json
from pathlib import Path

DATA_FILE = Path("zero-trust/policy/approved_versions.json")


def load_approved(path: Path | None = None) -> list[dict]:
    f = path or DATA_FILE
    return json.loads(f.read_text(encoding="utf-8"))["approved_versions"]


def model_approved(model: dict, approved: list[dict] | None = None) -> dict:
    """Return {'allow': bool, 'reason': str}. Mirrors the Rego rule exactly."""
    if approved is None:
        approved = load_approved()
    version = model.get("version")
    artifact_hash = model.get("artifact_hash")
    if not version or not artifact_hash:
        return {"allow": False, "reason": "model missing version or artifact_hash"}
    for a in approved:
        if a["version"] == version and a["artifact_hash"] == artifact_hash:
            return {"allow": True, "reason": f"approved {version}"}
    return {
        "allow": False,
        "reason": f"model version/hash not in approved set (version={version}, hash={artifact_hash[:20]}...)",
    }
