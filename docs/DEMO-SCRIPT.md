# Demo Script — 3-minute walkthrough

A narration plan for a screen-recorded walkthrough.

## 0:00–0:20 — The problem

Say: "Refinery AI fails in regulated environments not because the model is wrong, but because the evidence is missing. Which model produced this setpoint? What data did it see? Who approved it? Which control does it satisfy? This project answers all four."

## 0:20–0:50 — The architecture

On screen: architecture diagram in mermaid.live.

Say: "Five layers. Refining process at the bottom. OT DMZ where the AI agents live. Operator approval gate. Enterprise governance. Safety instrumented function outside the agent graph."

## 0:50–1:30 — The happy path

On screen: run python scripts/demo_pipeline.py.

Say: "Off-spec feedstock, color 3.6, spec is 1.0. Two agents propose corrections. Orchestrator ranks, checks bounds, mints evidence, signs. Verifier accepts. Apply recommendations, twin comes back on spec at 0.95 — deliberately below 1.0 because real advisors target margin."

## 1:30–2:00 — The attack matrix

On screen: run python scripts/demo_attacks.py, open docs/ATTACK-MATRIX.md.

Say: "Five attacks, five rejections. Replay caught by nonce. Tamper caught by signature. Unapproved model caught by policy. Stale timestamp caught by skew. Forged key caught by agent match."

## 2:00–2:20 — The network plane

On screen: run python scripts/demo_zones.py.

Say: "Second independent plane. Five legitimate flows allowed, six forbidden flows blocked. Even if the supervisory layer were compromised, it cannot reach the control layer."

## 2:20–2:50 — Evidence pipeline

On screen: Actions tab, both workflows green.

Say: "Evidence pipeline fails the build if a compliance row claims complete without an artifact, or if code references an unapproved model hash. Compliance is a CI check, not a document."

## 2:50–3:00 — Limitations

Say: "Not deployed in a live refinery. Process is a digital twin. HSM is a stub. Safety layer is a boundary. All stated in docs/WHAT-IS-SIMULATED.md."
