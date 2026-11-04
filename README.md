# Trusted Multi-Agent AI Advisory for Vegetable Oil Refining
### A zero-trust OT architecture with signed inference and evidence-based AI compliance

## Two independent enforcement planes

| Plane | Mechanism | Rejects |
|---|---|---|
| **Cryptographic** | Ed25519 + model-version allowlist + nonce store + timestamp skew | forged signatures, replayed envelopes, unapproved models, stale envelopes |
| **Network** | IEC 62443 zone router with explicit conduit matrix | AI-to-PLC, enterprise-to-control, supervisory-to-field |

## Safety boundary

The AI is advisory. It has no write path to the PLC/DCS and is outside the IEC 61511 safety instrumented function. See docs/SAFETY-BOUNDARY.md.

## Documentation

- [Executive summary](docs/EXECUTIVE-SUMMARY.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Safety boundary](docs/SAFETY-BOUNDARY.md)
- [What is simulated vs real](docs/WHAT-IS-SIMULATED.md)
- [Attack matrix](docs/ATTACK-MATRIX.md)
- [Demo script](docs/DEMO-SCRIPT.md)
- [Portfolio notes](docs/PORTFOLIO-NOTES.md)
