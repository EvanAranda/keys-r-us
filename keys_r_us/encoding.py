from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic

from mnemonic import Mnemonic

TEncoded = TypeVar('TEncoded')


class AbstractEncoding(Generic[TEncoded], ABC):

    @property
    @abstractmethod
    def encoding_name(self): ...


class AbstractDecoder(Generic[TEncoded], AbstractEncoding[TEncoded], ABC):

    @abstractmethod
    def decode(self, media: TEncoded) -> bytes:
        """
        Convert an encoded (encrypted) secret into the raw encrypted bytes of the secret.
        :param media:
        :return:
        """


class AbstractEncoder(Generic[TEncoded], AbstractEncoding[TEncoded], ABC):

    @abstractmethod
    def encode(self, seed: bytes) -> TEncoded:
        pass


@dataclass
class MnemonicAndPassphrase:
    mnemonic: str
    passphrase: str


class BipMnemonicEncoding(AbstractDecoder[MnemonicAndPassphrase]):

    def __init__(self, lang='english'):
        self._mnemonic = Mnemonic(lang)

    @property
    def encoding_name(self):
        return 'BIP39 Mnemonic'

    def decode(self, media: MnemonicAndPassphrase) -> bytes:
        return self._mnemonic.to_seed(media.mnemonic, media.passphrase)

    def set_lang(self, lang: str):
        self._mnemonic = Mnemonic(lang)


class SlipMnemonicEncoding(AbstractEncoder[MnemonicAndPassphrase],
                           AbstractDecoder[MnemonicAndPassphrase]):

    @property
    def encoding_name(self):
        return 'SLIP39 Mnemonic'

    def encode(self, seed: bytes) -> TEncoded:
        pass

    def decode(self, media: TEncoded) -> bytes:
        pass


class StringEncoding(AbstractEncoder[str],
                     AbstractDecoder[str]):

    @property
    def encoding_name(self):
        return 'Raw'

    def encode(self, seed: bytes) -> TEncoded:
        pass

    def decode(self, media: TEncoded) -> bytes:
        pass


class QREncoding(AbstractEncoder, AbstractDecoder):

    @property
    def encoding_name(self):
        return 'QR Code'

    def encode(self, seed: bytes) -> TEncoded:
        pass

    def decode(self, media: TEncoded) -> bytes:
        pass
