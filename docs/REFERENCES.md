# References

Every quantitative claim and standards alignment in this repository is
listed here with the source it rests on. If a claim is not backed by a
source below, it is either a modelling assumption (stated as such) or a
target (stated as such), not a measurement.

## Process baselines

### Bleaching earth reduction (up to ~6%)

**Claim in repo:** the quality advisory targets up to ~6% bleaching earth
reduction at equivalent or improved color.

**Status:** indicative target based on published refining-industry
efficiency reports and vendor case studies, not a controlled trial on
this unit.

**References:**
- O'Brien, R.D. *Fats and Oils: Formulating and Processing for
  Applications*, 3rd ed., CRC Press, 2008 — Chapter on bleaching
  discusses earth dosing practice and color targets.
- Gunstone, F.D. (ed.) *Vegetable Oils in Food Technology: Composition,
  Properties and Uses*, 2nd ed., Wiley-Blackwell, 2011 — background on
  bleaching earth consumption and process control.

### Deodorization steam reduction (1–5%)

**Claim in repo:** the energy advisory targets 1–5% deodorization steam
reduction while maintaining FFA and tocopherol specs.

**Status:** indicative range, consistent with published deodorization
control and heat-recovery literature. Not a measured result on this unit.

**References:**
- Gunstone, F.D. (ed.) *Vegetable Oils in Food Technology*, 2nd ed.,
  Wiley-Blackwell, 2011 — deodorization chapter covers stripping steam,
  time-temperature integral, and tocopherol retention trade-offs.
- O'Brien, R.D. *Fats and Oils*, 3rd ed., CRC Press, 2008 —
  deodorization process economics and utility consumption.

### Color, phosphorus, FFA targets

**Status:** representative industry spec values used to drive the digital
twin. Sourced from the two references above. These are the values a real
unit would be told by QA, not measurements from a live plant.

## Standards

### IEC 62443-3-2 and 3-3

- **IEC 62443-3-2:2020** — *Security for industrial automation and
  control systems — Part 3-2: Security risk assessment for system design*.
- **IEC 62443-3-3:2013** — *Part 3-3: System security requirements and
  security levels*.

Used for: zone and conduit definition, security level (SL) targets per
zone. See `compliance/iec62443/sl-justification.md`.

### IEC 61511

- **IEC 61511-1:2016+AMD1:2017** — *Functional safety: Safety
  instrumented systems for the process industry sector*.

Used for: the safety boundary statement. The AI advisory system is
explicitly outside the safety instrumented function. See
`docs/SAFETY-BOUNDARY.md`.

### NIST SP 800-82

- **NIST SP 800-82 Rev. 3 (2023)** — *Guide to Operational Technology
  (OT) Security*. (Earlier draft Rev. 4 should not be cited as a
  published standard.)

Used for: OT security posture and the acknowledgment that zero trust in
OT is a Level 3-and-above proposition, not a control-loop proposition.

### NIST SP 800-207

- **NIST SP 800-207 (2020)** — *Zero Trust Architecture*.

Used for: zero-trust principles (per-request verification, least
privilege, no implicit trust based on network location), **adapted** for
OT constraints. NIST itself notes the OT adaptation is not direct; this
repo's zero-trust enforcement operates at the DMZ boundary, not at the
controller.

### ISO/IEC 42001

- **ISO/IEC 42001:2023** — *Information technology — Artificial
  intelligence — Management system*.

Used for: AI management system structure, control-to-evidence matrix in
`compliance/iso42001/control-matrix.yaml`. Note: control numbering must
be verified against the licensed copy before external audit; the matrix
in this repo is a structural mapping, not a certification.

### NIST AI Risk Management Framework

- **NIST AI RMF 1.0 (2023)** — *Artificial Intelligence Risk Management
  Framework*.
- **NIST AI 600-1 (2024)** — *Generative AI Profile*.

Used for: function mapping in `compliance/nist-ai-rmf/function-mapping.md`.

## What is not claimed

- No claim of certification or conformance. This repository is a
  reference architecture and a simulated implementation.
- No claim of measured savings. The 6% and 1–5% figures are targets
  drawn from literature, not results.
- No claim of production safety. The AI is advisory; the safety
  instrumented function is independent.

## How to update this file

Every numeric claim in a README, doc, or code comment must point here.
If a claim has no source, either find one or soften it to a target with
a stated basis.
