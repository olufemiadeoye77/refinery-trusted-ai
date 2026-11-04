# Portfolio Notes — How This Project Maps to Roles

This project was built as a portfolio artifact for overlapping role families.

## Enterprise architecture roles

Reviewers ask: can you translate a business constraint into a defensible architectural decision?

Evidence:
- architecture/diagrams/integrated-architecture.mmd — full process-to-governance view
- architecture/zones-conduits.yaml — IEC 62443 segmentation as code
- docs/SAFETY-BOUNDARY.md — explicit scope discipline
- compliance/iso42001/control-matrix.yaml — controls mapped to artifacts

Talking point: I designed the architecture so the AI is provably outside the safety boundary. That decision — not the AI — is what makes this deployable.

## Industrial AI engineering roles

Reviewers ask: do you build AI that respects process constraints?

Evidence:
- process/twin/units/bleaching.py, deodorization.py — published baselines in the process model
- agents/quality_agent/agent.py — targets 95% of spec, not 100%
- agents/energy_agent/agent.py — refuses to optimize utilities when product is off-spec
- agents/orchestrator/agent.py — bounds-checking, ranking, evidence binding, signing

Talking point: The energy agent returns zero proposals when product is off-spec. Real refinery AI has to know when not to act.

## OT cybersecurity roles

Reviewers ask: do you understand signing is not authorization?

Evidence:
- zero-trust/verifier/verifier.py — eight-stage fail-closed verification
- zero-trust/verifier/nonce_store.py — replay protection
- zero-trust/policy/model-allowlist.rego — policy separate from crypto
- zero-trust/lab/zone_router.py — IEC 62443 conduit enforcement
- docs/ATTACK-MATRIX.md — each attack to the stage that catches it

Talking point: The attack matrix is the important artifact. Each attack class fails at a specific, logged stage.

## AI compliance roles

Reviewers ask: does your compliance story survive an audit?

Evidence:
- .github/workflows/evidence-pipeline.yml — compliance enforced in CI
- compliance/iso42001/control-matrix.yaml — every complete row points to a real artifact
- zero-trust/policy/approved_versions.json — model allowlist is the governance artifact

Talking point: The evidence pipeline fails the build if a compliance row claims complete without an artifact.
