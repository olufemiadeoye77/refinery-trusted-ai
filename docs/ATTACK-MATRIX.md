# Zero-Trust Verification: Attack Matrix

Every advisory envelope passes through six verification stages. This
table documents each attack that the system rejects and the stage that
catches it. Run `python scripts/demo_attacks.py` to reproduce.

| # | Attack | Stage caught | Detector |
|---|---|---|---|
| 1 | Replay of a valid envelope | `nonce` | `NonceStore` remembers seen nonces; recorded only after signature passes |
| 2 | Tampered recommendation value | `signature` | Ed25519 signature over canonical payload fails |
| 3 | Unapproved model version (signed correctly) | `policy` | `approved_versions.json` allowlist rejects version+hash not on list |
| 4 | Stale timestamp (10 min old) | `freshness` | Skew window of 300 s; anything older is refused |
| 5 | Forged key_id (agent claim ≠ key) | `agent_match` | Agent claim must equal the agent owning the key |
| – | Happy path (control) | `ok` | Accepted and recorded |

## Verification order (fail-closed at every step)

1. `signature_present` — a signature block exists, alg is Ed25519
2. `signature_alg` — alg is the expected one
3. `key_registry` — key_id maps to a known agent
4. `agent_match` — agent claim matches key owner
5. `signature` — Ed25519 verification passes
6. `policy` — model version and artifact hash on the allowlist
7. `freshness` — `issued_at` within skew window
8. `nonce` — nonce not seen before; record only after all above pass

Recording the nonce *after* signature verification (not before) prevents
an attacker from poisoning the store with unsigned garbage.
