"""End-to-end demo:
1. Run twin with defaults (off-spec).
2. Run each agent, collect proposals.
3. Orchestrator ranks, checks bounds, mints evidence, signs.
4. Verifier accepts each signed envelope.
5. Apply accepted recommendations to twin -> should be on-spec.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "zero-trust"))
sys.path.insert(0, str(ROOT / "process"))

from twin.train_model import simulate  # noqa: E402
from agents.quality_agent.agent import propose as quality_propose  # noqa: E402
from agents.energy_agent.agent import propose as energy_propose  # noqa: E402
from agents.maintenance_agent.agent import propose as maintenance_propose  # noqa: E402
from agents.orchestrator.agent import Orchestrator  # noqa: E402
from verifier.verifier import verify_envelope  # noqa: E402


def main() -> int:
    print("=== 1. BASELINE (off-spec feed, default setpoints) ===")
    state = simulate()
    print(json.dumps({
        "overall_quality_ok": state["overall_quality_ok"],
        "finished_oil": state["finished_oil"],
    }, indent=2))
    assert state["overall_quality_ok"] is False, "baseline should be off-spec for the demo"

    print("\n=== 2. AGENT PROPOSALS ===")
    proposals_by_agent = {
        "quality": quality_propose(state),
        "energy": energy_propose(state),
        "maintenance": maintenance_propose(state),
    }
    for agent, props in proposals_by_agent.items():
        print(f"{agent}: {len(props)} proposal(s)")
        for p in props:
            print(f"  - {p['variable']}: {p['current_value']} -> {p['proposed_value']} "
                  f"({p['rationale']})")

    print("\n=== 3. ORCHESTRATOR: rank, bound-check, attest, sign ===")
    orch = Orchestrator()
    envelopes = orch.produce_package(proposals_by_agent)
    print(f"signed envelopes: {len(envelopes)}")
    for env in envelopes:
        print(f"  {env['signature']['key_id']} | {env['recommendation']['variable']} | "
              f"evidence={env['evidence_ref']}")

    print("\n=== 4. VERIFIER: accept each envelope ===")
    for env in envelopes:
        result = verify_envelope(env)
        print(f"  {env['recommendation']['variable']}: {result}")
        assert result["ok"] is True, f"verification failed: {result}"

    print("\n=== 5. APPLY ACCEPTED RECOMMENDATIONS, RE-RUN TWIN ===")
    overrides = {}
    for env in envelopes:
        var = env["recommendation"]["variable"]
        val = env["recommendation"]["proposed_value"]
        if var == "acid_dose_kg_per_t":
            overrides["acid_dose_kg_per_t"] = val
        elif var == "earth_dose_kg_per_t":
            overrides["earth_dose_kg_per_t"] = val
        elif var == "deod_steam_kg_per_t":
            overrides["deod_steam_kg_per_t"] = val
        # maintenance RUL is advisory only; not applied to process

    state2 = simulate(**overrides)
    print(json.dumps({
        "applied": overrides,
        "overall_quality_ok": state2["overall_quality_ok"],
        "finished_oil": state2["finished_oil"],
    }, indent=2))
    assert state2["overall_quality_ok"] is True, "advisory should restore spec"

    print("\nOK: off-spec -> signed advisory -> verified -> on-spec")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
