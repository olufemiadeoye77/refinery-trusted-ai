# Executive Summary

**Trusted Multi-Agent AI Advisory for Vegetable Oil Refining**
A zero-trust OT architecture with signed inference and evidence-based AI compliance.

## What this is

A reference architecture and working implementation of a multi-agent AI
advisory system for the degumming–neutralization–bleaching–deodorization
train of a vegetable oil refinery. Every AI recommendation is signed,
version-pinned, policy-authorized, human-approved, and bound to a
machine-generated compliance evidence record.

It is **not** a closed-loop controller. The AI is advisory. The safety
instrumented function (IEC 61511) is outside the agent graph and remains
fully functional if the AI layer is removed.

## What it proves

Two independent enforcement planes, both tested in CI on every push:

| Plane | Mechanism | Rejects |
|---|---|---|
| **Cryptographic** | Ed25519 signature + model-version allowlist (OPA-style policy) + nonce store + timestamp skew | forged signatures, replayed envelopes, unapproved models, stale envelopes |
| **Network** | Zone router with explicit conduit matrix (IEC 62443) | AI→PLC, enterprise→control, supervisory→field |

Plus an **evidence pipeline** that fails the build if any compliance row
declares `complete` without a corresponding artifact, or if any model
hash referenced in code is not on the approved list.

## How to verify in 60 seconds

```bash
git clone https://github.com/olufemiadeoye77/refinery-trusted-ai
cd refinery-trusted-ai
pip install -r requirements.txt

python scripts/demo_pipeline.py    # off-spec -> signed advisory -> on-spec
python scripts/demo_attacks.py     # 5 attacks rejected
python scripts/demo_zones.py       # 6 forbidden flows blocked
