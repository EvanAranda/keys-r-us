from di_ioc import ServiceContainer, auto

from keys_r_us.encoding import BipMnemonicEncoding, StringEncoding, QREncoding, SlipMnemonicEncoding, \
    AbstractEncoding
from keys_r_us.spec import AbstractSpec, BipSpec, SlipSpec
from .abstract import ViewFor
from .decoder import DecoderSelector, RawSeedDecoder, SlipMnemonicDecoder, BipMnemonicDecoder
from .spec import SpecSelector, BipSpecInput, SlipSpecInput


class LibServices(ServiceContainer):
    def __init__(self):
        super().__init__()

        specs = [BipSpec, SlipSpec]
        for spec in specs:
            self[[AbstractSpec, spec]] = auto(spec)

        encodings = [StringEncoding, SlipMnemonicEncoding, BipMnemonicEncoding, QREncoding]
        for enc in encodings:
            self[[AbstractEncoding, enc]] = auto(enc)


class AppServices(ServiceContainer):
    def __init__(self):
        super().__init__()

        # selectors (tabs)
        self[SpecSelector] = auto(SpecSelector)
        self[DecoderSelector] = auto(DecoderSelector)

        # specs
        self[[ViewFor[BipSpec], BipSpecInput]] = auto(BipSpecInput)
        self[[ViewFor[SlipSpec], SlipSpecInput]] = auto(SlipSpecInput)

        # decoders
        self[[ViewFor[BipMnemonicEncoding], BipMnemonicDecoder]] = auto(BipMnemonicDecoder)
        self[[ViewFor[SlipMnemonicEncoding], SlipMnemonicDecoder]] = auto(SlipMnemonicDecoder)
        self[[ViewFor[StringEncoding], RawSeedDecoder]] = auto(RawSeedDecoder)

        self.register(LibServices())
