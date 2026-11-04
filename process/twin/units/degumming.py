"""Degumming: water/acid degumming of crude vegetable oil.

Predicts residual phosphorus after degumming from feed phosphorus,
acid dose, water dose, and contact temperature. Acid degumming can
achieve >99% phosphorus removal at optimal dosing; we model the
ceiling at 99.5% rather than 99.0%, matching published data and
giving the advisory layer realistic headroom.
"""

from dataclasses import dataclass


@dataclass
class DegummingInputs:
    feed_phosphorus_ppm: float
    acid_dose_kg_per_t: float = 0.8
    water_dose_pct: float = 3.0
    temperature_c: float = 65.0


@dataclass
class DegummingOutputs:
    residual_phosphorus_ppm: float
    gum_yield_pct: float
    within_spec: bool


def model(inp: DegummingInputs, target_ppm: float = 5.0) -> DegummingOutputs:
    # Removal efficiency rises with acid dose, ceiling at 99.5%
    removal_eff = min(0.995, 0.80 + 0.15 * min(inp.acid_dose_kg_per_t, 1.5))
    temp_penalty = 1.0 - 0.02 * abs(inp.temperature_c - 65.0)
    temp_penalty = max(0.7, min(1.0, temp_penalty))
    residual = inp.feed_phosphorus_ppm * (1.0 - removal_eff * temp_penalty)
    gum_yield = 0.4 + 0.3 * inp.water_dose_pct / 3.0
    return DegummingOutputs(
        residual_phosphorus_ppm=round(residual, 3),
        gum_yield_pct=round(gum_yield, 3),
        within_spec=residual <= target_ppm,
    )
