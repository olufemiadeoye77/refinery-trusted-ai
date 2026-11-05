# IEC 62443 Security Level Justification

This file justifies the security level (SL) targets assigned to each
zone in `architecture/zones-conduits.yaml`.

## Scope

The assessment covers a single refining train (degumming → neutralization
→ bleaching → deodorization) and the surrounding IT/OT boundary. It does
not cover a full refinery network. See `docs/WHAT-IS-SIMULATED.md`.

## SL definitions (IEC 62443-3-3)

IEC 62443-3-3 defines four security levels based on the capability of a
threat actor:

- **SL 1** — protection against casual or coincidental violation
- **SL 2** — protection against intentional violation using simple means
- **SL 3** — protection against intentional violation using sophisticated
  means with moderate resources
- **SL 4** — protection against intentional violation using sophisticated
  means with extended resources

## Targets per zone

### Z0/Z1 — Field and Control (SL 3)

The controller and field devices are the highest-consequence zone for
process safety. A compromise can cause physical harm. SL 3 is the
realistic target for a well-run refining site; SL 4 is rare outside
nuclear/defence. Primary protection is zone-boundary defence, not
zero-trust inside the control loop (NIST SP 800-82 Rev. 3 acknowledges
that ZT cannot be enforced inside many controllers).

### Z2 — Supervisory (SL 3)

HMIs, historian, engineering workstation. Compromise here can cascade
into control if the boundary between Z2 and Z1 is weak. SL 3 matches Z1
because the consequence is similar: an attacker on the HMI can often
reach the controller. This is precisely why the ZT enforcement point
sits between Z2 and Z3.5, not inside Z2.

### Z3.5 — OT DMZ / AI Advisory (SL 3)

Hosts the agents, verifier, and model cache. Compromise here must not
lead to control-layer access — that is what the zone router enforces
(documented in `zero-trust/lab/conduits.yaml`). SL 3 is consistent with
the DMZ's role as a semi-trusted intermediary.

### Z4 — Enterprise / Governance (SL 2)

Model registry, risk register, compliance evidence, training pipeline.
Compromise is serious (model tampering, evidence loss) but does not
directly reach the process. SL 2 is the realistic target for a corporate
IT zone that a refining site can actually sustain.

## Why not higher SLs

- **SL 4** requires formal verification, cryptographic protection of
  every control-layer protocol, and a staffing level most refining sites
  cannot sustain. It is aspirational, not deployable at typical scale.
- The strength of this architecture is not maximum SL on any single
  zone — it is the independence of enforcement planes (crypto, network,
  evidence) and the fail-closed posture at the DMZ boundary.

## What is not claimed

This file is a *design justification*, not a certified SL assessment.
A real IEC 62443-3-2 assessment would require a site-specific risk
assessment including threat actor capability, consequence analysis, and
asset inventory — none of which this repo has. See
`docs/WHAT-IS-SIMULATED.md`.

## References

- IEC 62443-3-2:2020 — security risk assessment for system design
- IEC 62443-3-3:2013 — system security requirements and security levels
- NIST SP 800-82 Rev. 3 (2023) — OT security guidance
