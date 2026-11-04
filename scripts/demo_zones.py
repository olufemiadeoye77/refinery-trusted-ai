"""Zone enforcement demo.

Legitimate flows must be ALLOWED. Forbidden flows must be BLOCKED.
Both are asserted so any regression in the conduit matrix fails CI.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "zero-trust"))

from lab.zone_router import ZoneRouter  # noqa: E402


LEGIT = [
    ("Z0_FIELD", "Z2_SUPERVISORY", "process telemetry to historian"),
    ("Z2_SUPERVISORY", "Z35_DMZ", "historian read to agents"),
    ("Z35_DMZ", "Z2_SUPERVISORY", "signed advisory to operator"),
    ("Z4_GOVERNANCE", "Z35_DMZ", "model deployment to DMZ"),
    ("Z35_DMZ", "Z4_GOVERNANCE", "evidence egress to governance"),
]

FORBIDDEN = [
    ("Z35_DMZ", "Z1_CONTROL", "AI trying to write to PLC"),
    ("Z35_DMZ", "Z0_FIELD", "AI trying to reach field devices"),
    ("Z4_GOVERNANCE", "Z1_CONTROL", "enterprise bypass to control"),
    ("Z4_GOVERNANCE", "Z0_FIELD", "enterprise bypass to field"),
    ("Z2_SUPERVISORY", "Z0_FIELD", "supervisory bypass to field"),
    ("Z1_CONTROL", "Z4_GOVERNANCE", "control layer pushing data to enterprise"),
]


def main() -> int:
    router = ZoneRouter()

    print("=== LEGITIMATE FLOWS (expect ALLOW) ===")
    for src, dst, label in LEGIT:
        d = router.check(src, dst)
        status = "ALLOW" if d.allowed else "DENY "
        print(f"  {status}  {src:16s} -> {dst:16s}  {label}  [{d.reason}]")
        assert d.allowed, f"expected allow: {src}->{dst}: {d.reason}"

    print("\n=== FORBIDDEN FLOWS (expect DENY) ===")
    for src, dst, label in FORBIDDEN:
        d = router.check(src, dst)
        status = "ALLOW" if d.allowed else "DENY "
        print(f"  {status}  {src:16s} -> {dst:16s}  {label}  [{d.reason}]")
        assert not d.allowed, f"expected deny: {src}->{dst}: {d.reason}"

    print("\nOK: 5 legitimate flows allowed, 6 forbidden flows blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
