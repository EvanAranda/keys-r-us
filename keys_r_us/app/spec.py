from typing import Sequence, Iterable

from di_ioc.container import BasicRequest
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static

from keys_r_us.encoding import BipMnemonicEncoding, AbstractDecoder, StringEncoding, SlipMnemonicEncoding
from keys_r_us.spec import AbstractSpec, BipSpec, SlipSpec
from .abstract import ViewFor, app_services
from .decoder import DecoderSelector, Decoder
from .widgets import Tabs


class SpecSelector(Tabs[AbstractSpec]):

    def __init__(self, specs: Sequence[AbstractSpec]):
        super().__init__(specs)
        self.specs = specs

    def compose_header(self, item: AbstractSpec) -> str:
        return item.name

    def compose_content(self, item: AbstractSpec) -> ComposeResult:
        """
        Asks the service provider for a widget that can render the spec.
        :param item:
        :return:
        """
        req = BasicRequest(ViewFor[type(item)], args={'spec': item})
        yield app_services(self).get_required_service(req)


class SpecInput(Widget):
    DEFAULT_CSS = """
    SpecInput {
        layout: grid; 
        grid-size: 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield DecoderSelector(self.supported_encodings())
        yield from self.compose_output()

    def supported_encodings(self) -> Iterable[AbstractDecoder]:
        raise NotImplementedError()

    def compose_output(self) -> ComposeResult:
        raise NotImplementedError()

    def on_decoder_decoded(self, e: Decoder.Decoded):
        pass


class BipSpecInput(SpecInput, ViewFor[BipSpec]):

    def __init__(self, spec: BipSpec):
        super().__init__()
        self.spec = spec

    def supported_encodings(self) -> Iterable[AbstractDecoder]:
        services = app_services(self)
        yield services.get_required_service(BipMnemonicEncoding)
        yield services.get_required_service(StringEncoding)
        # yield services.get_required_service(QREncoding)

    def compose_output(self) -> ComposeResult:
        yield Static('The output')


class SlipSpecInput(SpecInput, ViewFor[SlipSpec]):

    def __init__(self, spec: SlipSpec):
        super().__init__()
        self.spec = spec

    def supported_encodings(self) -> Iterable[AbstractDecoder]:
        services = app_services(self)
        yield services.get_required_service(SlipMnemonicEncoding)
        yield services.get_required_service(StringEncoding)
        # yield services.get_required_service(QREncoding)

    def compose_output(self) -> ComposeResult:
        yield from ()
