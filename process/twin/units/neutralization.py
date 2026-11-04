"""Neutralization: alkali neutralization of free fatty acids.

Alkali dose is the key controllable variable. Under-dosing leaves FFA
above spec; over-dosing increases soapstock and neutral oil loss and
reduces downstream natural antioxidant retention.
"""

from dataclasses import dataclass


@dataclass
class NeutralizationInputs:
    ffa_in_pct: float
    alkali_dose_kg_per_t: float = 6.0
    temperature_c: float = 85.0


@dataclass
class NeutralizationOutputs:
    ffa_out_pct: float
    soapstock_pct: float
    neutral_oil_loss_pct: float
    within_spec: bool


def model(inp: NeutralizationInputs, target_ffa_pct: float = 0.05) -> NeutralizationOutputs:
    # Excess alkali factor: minimum required is proportional to FFA
    min_alkali = 1.2 * inp.ffa_in_pct * 10  # heuristic kg/t per % FFA
    excess = max(0.0, inp.alkali_dose_kg_per_t - min_alkali)
    # FFA removal saturates once excess is positive
    if excess > 0:
        ffa_out = max(0.005, inp.ffa_in_pct * 0.02)
    else:
        ffa_out = inp.ffa_in_pct * (1.0 - inp.alkali_dose_kg_per_t / max(min_alkali, 1e-6))
    soapstock = 0.15 * inp.ffa_in_pct + 0.02 * excess
    oil_loss = 0.4 * soapstock
    return NeutralizationOutputs(
        ffa_out_pct=round(ffa_out, 4),
        soapstock_pct=round(soapstock, 4),
        neutral_oil_loss_pct=round(oil_loss, 4),
        within_spec=ffa_out <= target_ffa_pct,
    )
