"""Zone router: enforce IEC 62443 conduit rules on any zone-to-zone message.

Every message must declare a source zone, destination zone, and intent.
The router returns a Decision (allowed, reason, conduit_id). Deny by default.
"""

from dataclasses import dataclass
from pathlib import Path

CONDUITS_FILE = Path("zero-trust/lab/conduits.yaml")


@dataclass
class Decision:
    allowed: bool
    reason: str
    conduit_id: str | None = None


def _load() -> dict:
    import yaml
    return yaml.safe_load(CONDUITS_FILE.read_text(encoding="utf-8"))


class ZoneRouter:
    def __init__(self, config: dict | None = None) -> None:
        self.config = config or _load()

    def check(self, src: str, dst: str, intent: str = "generic") -> Decision:
        for f in self.config.get("forbidden", []):
            if f["from"] == src and f["to"] == dst:
                return Decision(False, f"forbidden: {f['reason']}", None)

        for c in self.config.get("conduits", []):
            if c["from"] == src and c["to"] == dst and c.get("allowed", False):
                return Decision(True, f"allowed by {c['id']}", c["id"])

        return Decision(False, f"no conduit from {src} to {dst}", None)
