import base58

from .interface import SecretEncoder


class Base58SecretEncoder(SecretEncoder):
    name = 'base58'
    desc = 'Base58 Encoding.'
    options = dict()

    @classmethod
    def encode(cls, secret: bytes, **opts) -> str:
        return base58.b58encode(secret).decode()

    @classmethod
    def decode(cls, encoded: str, **opts) -> bytes:
        return base58.b58decode(encoded)
