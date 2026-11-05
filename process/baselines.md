# Process Baselines

The digital twin in `process/twin/` uses the numbers below. Every number
here is either (a) a representative industry spec value with a source in
`docs/REFERENCES.md`, or (b) a modelling assumption stated as such. No
number is a measurement from a live plant.

## Feedstock (crude soybean oil, representative)

| Parameter | Value | Basis |
|---|---|---|
| Phosphorus | 500 ppm | modelling assumption, within typical crude range |
| Free fatty acid | 0.75% | modelling assumption |
| Color (Lovibond red) | 12.0 | modelling assumption |
| Tocopherol content | 0.12% | modelling assumption |

## Finished-oil targets (industry-typical)

| Parameter | Target | Basis |
|---|---|---|
| Phosphorus (after degumming) | ≤ 5 ppm | industry practice, see REFERENCES.md |
| Free fatty acid (finished) | ≤ 0.05% | industry practice |
| Color (finished, Lovibond red) | ≤ 1.0 | industry practice |
| Tocopherol retained | ≥ 0.10% | deodorization constraint |

## Utility baselines

| Parameter | Baseline | Notes |
|---|---|---|
| Bleaching earth | 8.0 kg/t | typical for soybean oil at this color load |
| Deodorization steam | 25.0 kg/t | typical for continuous deodorization |
| Deodorization temperature | 250 °C | within standard operating window |
| Deodorization time | 60 min | within standard operating window |

## Advisory targets (not measurements)

- **Bleaching earth:** target up to **6% reduction** at equivalent or
  improved color. Indicative target from published literature. Not a
  measured result on this unit. See `docs/REFERENCES.md`.
- **Deodorization steam:** target **1–5% reduction** while maintaining
  FFA and tocopherol specs. Indicative range. Not a measured result.
- **Quality advisory:** targets **95% of spec**, not 100%, to leave
  operational margin. This is a design decision, not an industry
  standard.

## What is not claimed

This repo does not claim to have achieved any of these numbers. The
demos run on a deterministic twin with fixed values. Real savings would
require plant validation, which is explicitly out of scope (see
`docs/WHAT-IS-SIMULATED.md`).
