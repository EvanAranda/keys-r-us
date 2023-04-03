from .interface import SecretEncoder


class HexSecretEncoder(SecretEncoder):
    name = 'hex'
    desc = 'Hex (base16) encoding.'
    options = dict()

    @classmethod
    def encode(cls, secret: bytes, **opts) -> str:
        return secret.hex()

    @classmethod
    def decode(cls, encoded: str, **opts) -> bytes:
        return bytes.fromhex(encoded)
