"""Key management for the signing service.

Per-agent Ed25519 keypairs. Keys live in zero-trust/signing/keys/ which
is gitignored. Rotation policy: regenerate on every minor release.
"""

import os
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

AGENTS = ["quality", "energy", "maintenance", "orchestrator", "compliance"]

KEYS_DIR = Path(os.environ.get("KEYS_DIR", "zero-trust/signing/keys"))
KEYS_DIR.mkdir(parents=True, exist_ok=True)


def key_paths(agent: str) -> tuple[Path, Path]:
    return KEYS_DIR / f"{agent}.key", KEYS_DIR / f"{agent}.pub"


def ensure_keypair(agent: str) -> tuple[Path, Path]:
    if agent not in AGENTS:
        raise ValueError(f"unknown agent: {agent}")
    priv_path, pub_path = key_paths(agent)
    if priv_path.exists() and pub_path.exists():
        return priv_path, pub_path
    sk = Ed25519PrivateKey.generate()
    priv_path.write_bytes(sk.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    ))
    pub_path.write_bytes(sk.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ))
    return priv_path, pub_path
