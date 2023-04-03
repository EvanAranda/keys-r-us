import typing as t
from dataclasses import dataclass


@dataclass
class Option:
    """
    An option to control the encoding of a secret.
    """
    description: str
    default: t.Any
    ctor: t.Callable[[str], t.Any]
    is_flag: bool = False


@t.runtime_checkable
class SecretEncoder(t.Protocol):
    """
    An interface for encoding a secret as a string.
    """
    name: str
    desc: str
    options: t.Dict[str, Option]

    @classmethod
    def encode(cls, secret: bytes, **opts) -> str:
        """
        Encode a secret and return a string representation of it, which when passed to decode,
        will return the original secret.
        :param secret:
        :param opts:
        :return:
        """
        raise NotImplementedError()

    @classmethod
    def decode(cls, encoded: str, **opts) -> bytes:
        """
        Decode a string representation of a secret and return the original secret.
        :param encoded:
        :param opts:
        :return:
        """
        raise NotImplementedError()
