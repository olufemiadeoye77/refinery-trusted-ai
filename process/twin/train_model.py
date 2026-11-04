"""Full train model: degumming -> neutralization -> bleaching -> deodorization.

Produces a single dict of process state that advisory agents consume.
Deterministic given inputs; stochasticity is added in scenario runners.
"""

from __future__ import annotations

from dataclasses import asdict

from . import constants as C
from .units import bleaching, degumming, deodorization, neutralization


def simulate(
    feed_phosphorus_ppm: float = C.FEED_PHOSPHORUS_PPM,
    feed_ffa_pct: float = C.FEED_FFA_PCT,
    feed_color_red: float = C.FEED_COLOR_RED,
    feed_tocopherol_pct: float = 0.12,
    earth_dose_kg_per_t: float = C.BASELINE_BLEACHING_EARTH_KG_PER_T,
    deod_temp_c: float = C.BASELINE_DEOD_TEMP_C,
    deod_time_min: float = C.BASELINE_DEOD_TIME_MIN,
    deod_steam_kg_per_t: float = C.BASELINE_DEOD_STEAM_KG_PER_T,
    acid_dose_kg_per_t: float = 0.8,
    alkali_dose_kg_per_t: float = 6.0,
) -> dict:
    dg = degumming.model(
        degumming.DegummingInputs(
            feed_phosphorus_ppm=feed_phosphorus_ppm,
            acid_dose_kg_per_t=acid_dose_kg_per_t,
        ),
        target_ppm=C.TARGET_PHOSPHORUS_PPM,
    )

    nu = neutralization.model(
        neutralization.NeutralizationInputs(
            ffa_in_pct=feed_ffa_pct,
            alkali_dose_kg_per_t=alkali_dose_kg_per_t,
        ),
        target_ffa_pct=0.5,  # intermediate target; deodorization finishes the job
    )

    bl = bleaching.model(
        bleaching.BleachingInputs(
            color_in_red=feed_color_red,
            phosphorus_in_ppm=dg.residual_phosphorus_ppm,
            earth_dose_kg_per_t=earth_dose_kg_per_t,
        ),
        target_color_red=C.TARGET_COLOR_RED,
    )

    do = deodorization.model(
        deodorization.DeodorizationInputs(
            ffa_in_pct=nu.ffa_out_pct,
            tocopherol_in_pct=feed_tocopherol_pct,
            temperature_c=deod_temp_c,
            time_min=deod_time_min,
            steam_kg_per_t=deod_steam_kg_per_t,
        ),
        target_ffa_pct=C.TARGET_FFA_PCT,
        min_tocopherol_pct=C.TARGET_TOCOPHEROL_PCT,
    )

    return {
        "feed": {
            "phosphorus_ppm": feed_phosphorus_ppm,
            "ffa_pct": feed_ffa_pct,
            "color_red": feed_color_red,
            "tocopherol_pct": feed_tocopherol_pct,
        },
        "units": {
            "degumming": asdict(dg),
            "neutralization": asdict(nu),
            "bleaching": asdict(bl),
            "deodorization": asdict(do),
        },
        "utilities": {
            "bleaching_earth_kg_per_t": bl.earth_used_kg_per_t,
            "deodorization_steam_kg_per_t": do.steam_used_kg_per_t,
        },
        "finished_oil": {
            "color_red": bl.color_out_red,
            "ffa_pct": do.ffa_out_pct,
            "tocopherol_pct": do.tocopherol_out_pct,
        },
        "overall_quality_ok": all([
            dg.within_spec, bl.within_spec, do.within_spec,
        ]),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(simulate(), indent=2))
