"""Nonce store for replay protection.

In-memory for the demo. In production this is Redis or a durable KV
store with a TTL equal to the envelope acceptance window. Nonces are
only recorded AFTER signature verification succeeds, so an attacker
cannot poison the store with unsigned garbage.
"""


class NonceStore:
    def __init__(self) -> None:
        self._seen: set[str] = set()

    def seen(self, nonce: str) -> bool:
        return nonce in self._seen

    def record(self, nonce: str) -> None:
        self._seen.add(nonce)

    def __len__(self) -> int:
        return len(self._seen)
