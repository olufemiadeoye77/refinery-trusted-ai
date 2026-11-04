"""Deodorization: steam stripping of FFA and volatiles under vacuum.

The controllable trade-off: higher temperature and longer time strip
more FFA but degrade tocopherols (natural antioxidants) and consume
more steam. Published data shows 1-5% steam reduction is achievable
with better-controlled time-temperature integral.
"""

from dataclasses import dataclass


@dataclass
class DeodorizationInputs:
    ffa_in_pct: float
    tocopherol_in_pct: float
    temperature_c: float = 250.0
    time_min: float = 60.0
    steam_kg_per_t: float = 25.0


@dataclass
class DeodorizationOutputs:
    ffa_out_pct: float
    tocopherol_out_pct: float
    steam_used_kg_per_t: float
    within_spec: bool


def model(
    inp: DeodorizationInputs,
    target_ffa_pct: float = 0.05,
    min_tocopherol_pct: float = 0.10,
) -> DeodorizationOutputs:
    # Time-temperature integral drives stripping and degradation
    tti = (inp.temperature_c / 250.0) * (inp.time_min / 60.0)
    ffa_out = max(0.005, inp.ffa_in_pct * pow(0.10, tti))
    tocopherol_out = max(0.0, inp.tocopherol_in_pct * pow(0.85, tti))
    within = (ffa_out <= target_ffa_pct) and (tocopherol_out >= min_tocopherol_pct)
    return DeodorizationOutputs(
        ffa_out_pct=round(ffa_out, 4),
        tocopherol_out_pct=round(tocopherol_out, 4),
        steam_used_kg_per_t=inp.steam_kg_per_t,
        within_spec=within,
    )
