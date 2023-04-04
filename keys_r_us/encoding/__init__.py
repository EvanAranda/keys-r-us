import typing as t

from .base58 import Base58SecretEncoder
from .hex import HexSecretEncoder
from .interface import SecretEncoder
from .qr import QRSecretEncoder

formats = [
    QRSecretEncoder,
    HexSecretEncoder,
    Base58SecretEncoder]

_formats_table: t.Dict[str, SecretEncoder] = {fmt.name: fmt for fmt in formats}


def get_encoding(name: str) -> SecretEncoder:
    enc = _formats_table.get(name)
    if enc is None:
        raise RuntimeError(f'{name} is not an encoding.')
    return enc


def get_opts(encoding: t.Type[SecretEncoder], opts: dict) -> dict:
    return {
        k: opts.get(k, encoding.options[k].default)
        for k, v in encoding.options.items()
    }


def encode(secret: bytes, encoding: t.Union[str, SecretEncoder], **opts) -> str:
    if isinstance(encoding, str):
        encoding = get_encoding(encoding)
    return encoding.encode(secret, **get_opts(encoding, opts))


def decode(encoded: str, encoding: t.Union[str, SecretEncoder], **opts) -> bytes:
    if isinstance(encoding, str):
        encoding = get_encoding(encoding)
    return encoding.decode(encoded, **get_opts(encoding, opts))
