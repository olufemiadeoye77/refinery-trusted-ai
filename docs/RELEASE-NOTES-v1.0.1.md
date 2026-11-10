# v1.0.1 — Visual Evidence Layer

Follow-up to v1.0.0. No changes to the runtime architecture, agents, zero-trust planes, or compliance matrix. This release adds the visual and reference layer that makes the v1.0.0 work reviewable at a glance.

## What ships

### References audit
- docs/REFERENCES.md — every quantitative claim mapped to a real published source or explicitly marked as a target or modelling assumption
- process/baselines.md — populated with sourced numbers and stated assumptions (previously empty placeholder)
- compliance/iec62443/sl-justification.md — per-zone security level reasoning tied to IEC 62443-3-3 (previously empty placeholder)

### Charts (matplotlib, 140 DPI PNG)
- docs/figures/01-baseline-vs-advisory.png — off-spec to on-spec, visual proof the advisory loop works
- docs/figures/02-attack-matrix.png — one acceptance, five rejections, each attack shown against the stage that catches it
- docs/figures/03-zone-conduit-map.png — five zones, allowed and blocked conduits
- docs/figures/04-compliance-coverage.png — ISO/IEC 42001 matrix status counts
- scripts/generate_charts.py — deterministic generator; CI runs it on every push to prove charts are reproducible from code

### Diagrams (Mermaid source + rendered SVG)
- architecture/diagrams/advisory-sequence.mmd and .svg — end-to-end advisory flow: twin to agents to orchestrator to compliance to signer to verifier to operator to MOC
- architecture/diagrams/verifier-stages.mmd and .svg — eight-stage fail-closed verification with reject paths
- Both SVG renders are embedded in the README

### Figures index
- docs/FIGURES.md — one-line description of every visual asset in the repo, with source location and usage guidance

### README
- New Visual evidence section embedding 4 charts and 2 SVG diagrams
- Documentation list expanded with links to References and Figures index

### CI
- New step Generate charts (reproducibility) runs scripts/generate_charts.py on every push
## What did not change

- Agents, orchestrator, compliance agent — unchanged
- Zero-trust cryptographic plane (Ed25519, policy, nonce, skew) — unchanged
- Zero-trust network plane (zone router) — unchanged
- ISO/IEC 42001 control matrix — unchanged
- Safety boundary — unchanged
- All four demo scripts still pass; attack matrix still rejects 5/5

## Verify

    pip install -r requirements.txt
    python scripts/demo_signing.py
    python scripts/demo_pipeline.py
    python scripts/demo_attacks.py
    python scripts/demo_zones.py
    python scripts/generate_charts.py

All four demos end in OK. Chart generation prints four wrote lines. Both workflows green on GitHub Actions.

## Honest limitations (unchanged from v1.0.0)

- Not deployed in a live refinery; the process is a digital twin
- The HSM is a software stub
- The safety layer is a boundary, not an implementation
- The 6% bleaching earth and 1-5% deodorization steam figures are literature-based targets, not measured results (see docs/REFERENCES.md)

## Standards (unchanged)

IEC 62443-3-2 / 3-3, IEC 61511, NIST SP 800-82 Rev. 3, NIST SP 800-207, ISO/IEC 42001:2023, NIST AI RMF 1.0.
