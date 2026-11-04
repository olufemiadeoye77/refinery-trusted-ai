"""Zero-trust enforcement point for advisory envelopes.

Checks: signature, key_id allowlist, agent identity, model version,
artifact hash, timestamp skew, nonce replay. Fail-closed by default.
"""
