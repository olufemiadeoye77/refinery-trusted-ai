"""Bleaching: adsorptive removal of color bodies and residual phosphorus.

Bleaching earth dose is the key controllable variable. Published
industrial data shows up to 6% earth reduction is achievable with
better-controlled dosing while improving color consistency.
"""

from dataclasses import dataclass


@dataclass
class BleachingInputs:
    color_in_red: float
    phosphorus_in_ppm: float
    earth_dose_kg_per_t: float = 8.0
    temperature_c: float = 95.0
    contact_time_min: float = 30.0


@dataclass
class BleachingOutputs:
    color_out_red: float
    residual_phosphorus_ppm: float
    earth_used_kg_per_t: float
    within_spec: bool


def model(inp: BleachingInputs, target_color_red: float = 1.0) -> BleachingOutputs:
    # Color removal is roughly first-order in earth dose up to saturation
    k = 0.15
    removal = 1.0 - pow(2.718, -k * inp.earth_dose_kg_per_t)
    removal *= min(1.0, inp.temperature_c / 95.0)
    removal *= min(1.0, inp.contact_time_min / 30.0)
    color_out = max(0.1, inp.color_in_red * (1.0 - removal))
    # Bleaching earth also strips residual phosphorus
    p_out = max(0.1, inp.phosphorus_in_ppm * (1.0 - 0.9 * removal))
    return BleachingOutputs(
        color_out_red=round(color_out, 3),
        residual_phosphorus_ppm=round(p_out, 3),
        earth_used_kg_per_t=inp.earth_dose_kg_per_t,
        within_spec=color_out <= target_color_red,
    )
