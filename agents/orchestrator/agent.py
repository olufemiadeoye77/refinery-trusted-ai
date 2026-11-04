"""Orchestrator: collects proposals from agents, checks bounds, mints
evidence via the compliance agent, and signs the final advisory envelope."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "zero-trust"))

from signing.signer import AdvisorySigner  # noqa: E402
from agents.compliance_agent.agent import attest  # noqa: E402

BOUNDS = {
    "earth_dose_kg_per_t": (5.0, 20.0),
    "acid_dose_kg_per_t": (0.5, 2.0),
    "deod_steam_kg_per_t": (18.0, 30.0),
    "bleaching_filter_rul_hours": (0.0, 1000.0),
}

MODEL = {
    "version": "0.1.0",
    "artifact_hash": "sha256:" + "b" * 64,
    "training_run": "run-2026-11-04-001",
}
INPUT_WINDOW = "2026-11-04T08:00:00Z/PT1H"


def _check_bounds(proposal: dict) -> tuple[float, bool, list[str]]:
    lo, hi = BOUNDS[proposal["variable"]]
    proposed = proposal["proposed_value"]
    violations: list[str] = []
    within = True
    if proposed < lo:
        violations.append(f"below lower bound {lo}")
        proposed = lo
        within = False
    if proposed > hi:
        violations.append(f"above upper bound {hi}")
        proposed = hi
        within = False
    return proposed, within, violations


class Orchestrator:
    def __init__(self) -> None:
        self.signer = AdvisorySigner("orchestrator")

    def produce_package(self, proposals_by_agent: dict[str, list[dict]]) -> list[dict]:
        flat: list[tuple[float, str, dict]] = []
        for agent, props in proposals_by_agent.items():
            for p in props:
                score = abs(p["proposed_value"] - p["current_value"]) * p["confidence"]
                flat.append((score, agent, p))
        flat.sort(reverse=True, key=lambda x: x[0])

        envelopes: list[dict] = []
        for score, agent, top in flat:
            proposed, within, violations = _check_bounds(top)
            recommendation = {
                "variable": top["variable"],
                "current_value": top["current_value"],
                "proposed_value": proposed,
                "confidence": top["confidence"],
            }
            evidence_ref = attest(top, MODEL, INPUT_WINDOW)
            payload = {
                "model": MODEL,
                "unit": top["unit"],
                "recommendation": recommendation,
                "constraints": {
                    "within_bounds": within,
                    "quality_preserved": within and not violations,
                    "violations": violations,
                },
                "provenance": {
                    "input_window": INPUT_WINDOW,
                    "model_card_ref": f"model-card-{top['variable']}-v0.1.0",
                },
                "evidence_ref": evidence_ref,
            }
            envelopes.append(self.signer.sign_envelope(payload))
        return envelopes
