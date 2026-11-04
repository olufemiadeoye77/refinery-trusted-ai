"""Quality agent: proposes setpoint changes to bring bleaching and
degumming back on spec. Uses its own local model of each unit (analytic
inverse) so the agent does not depend on the simulator.

Advisory targets below spec (95% of the target) to leave operational
margin. Targeting exactly at spec is bad industrial practice and would
put finished product right at the boundary.
"""

import math

# Safety margin: target 95% of spec to leave headroom
_SAFETY_FACTOR = 0.95


def _needed_earth_for_color(color_in_red: float, target_color_red: float = 1.0) -> float:
    target = target_color_red * _SAFETY_FACTOR  # 0.95
    if color_in_red <= target:
        return 8.0
    r_needed = 1.0 - target / color_in_red
    return round(-math.log(max(1e-6, 1.0 - r_needed)) / 0.15, 2)


def propose(state: dict) -> list[dict]:
    proposals: list[dict] = []
    feed = state["feed"]

    dg = state["units"]["degumming"]
    if not dg["within_spec"]:
        proposals.append({
            "unit": "degumming",
            "variable": "acid_dose_kg_per_t",
            "current_value": 0.8,
            "proposed_value": 1.5,
            "confidence": 0.78,
            "rationale": f"residual P {dg['residual_phosphorus_ppm']} ppm exceeds 5.0 target",
        })

    bl = state["units"]["bleaching"]
    if not bl["within_spec"]:
        needed = _needed_earth_for_color(feed["color_red"])
        proposals.append({
            "unit": "bleaching",
            "variable": "earth_dose_kg_per_t",
            "current_value": bl["earth_used_kg_per_t"],
            "proposed_value": needed,
            "confidence": 0.82,
            "rationale": f"color {bl['color_out_red']} Lovibond red exceeds 1.0 target; targeting 0.95 with margin",
        })

    return proposals
