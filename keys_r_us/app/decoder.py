from di_ioc.container import BasicRequest
from textual import events
from textual.app import ComposeResult
from textual.containers import Grid
from textual.message import Message, MessageTarget
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Input

from keys_r_us.encoding import BipMnemonicEncoding, AbstractDecoder, StringEncoding, SlipMnemonicEncoding, \
    MnemonicAndPassphrase
from .abstract import ViewFor, app_services
from .widgets import Tabs


class DecoderSelector(Tabs[AbstractDecoder]):
    """
    Selector to switch between different encoding options that can decode an encoded seed.
    """

    def compose_header(self, item: AbstractDecoder) -> str:
        return item.encoding_name

    def compose_content(self, item: AbstractDecoder) -> ComposeResult:
        """
        Asks the service container for a widget that renders the decoder.
        :param item:
        :return:
        """
        req = BasicRequest(ViewFor[type(item)], args={'decoder': item})
        yield app_services(self).get_required_service(req)


class Decoder(Widget):
    class Decoded(Message):
        def __init__(self, sender: MessageTarget, secret):
            self.secret = secret
            super().__init__(sender)

    class DecodeFailed(Message):
        def __init__(self, sender: MessageTarget, reason: str):
            self.reason = reason
            super().__init__(sender)

    def decoded(self, seed: bytes):
        self.emit(self.Decoded(self, seed))

    def decode_failed(self, err):
        self.emit(self.DecodeFailed(self, err))

    def try_decode(self) -> bytes:
        raise NotImplementedError()


class MnemonicWordInput(Input):
    def __init__(self, index: int):
        super().__init__()
        self.index = index

    def on_paste(self, event: events.Paste) -> None:
        pass


class MnemonicDecoder(Decoder):
    """
    Base class for mnemonic based decoders. Provides facilities to
    receive input as a list of words and attempts to decode
    when the list is changed.

    # Subclasses need to implement:
    :cvar self.try_decode: returns the decoded seed
    :cvar self.compose_options: available options to display to the user.
    """

    DEFAULT_CSS = """
    .options-grid {
        grid-size: 2; 
        grid-rows: 4;
        height: auto;
    }
    
    .mnemonic-grid {
        grid-size: 3;
        grid-rows: 4;
        height: auto;
    }
    
    MnemonicWordInput {
        margin: 1; 
    }
    
    .unused {
        display: none; 
    }
    """

    seed_phrase_len = reactive(24)
    words = reactive[str]('')

    def compose(self) -> ComposeResult:
        options_grid = Grid(*self.compose_options(), classes='options-grid')
        options_grid.shrink = True
        options_grid.expand = False
        yield options_grid
        yield Grid(
            *self.compose_word_inputs(),
            id='words',
            classes='mnemonic-grid')

    def compose_options(self) -> ComposeResult:
        yield Label('# of Words')
        yield Input(str(self.seed_phrase_len), id='seed_phrase_len')

    def compose_word_inputs(self) -> ComposeResult:
        for i in range(33):
            word_input = MnemonicWordInput(i)
            if i >= self.seed_phrase_len:
                word_input.add_class('unused')
            yield word_input

    def validate_seed_phrase_len(self, seed_phrase_len: int):
        return seed_phrase_len

    def watch_seed_phrase_len(self, seed_phrase_len: int):
        inputs = self.query(MnemonicWordInput)
        for idx, i in enumerate(inputs):
            if idx >= seed_phrase_len:
                i.add_class('unused')
            else:
                i.remove_class('unused')

    def watch_words(self, words: str):
        try:
            seed = self.try_decode()
            self.decoded(seed)
        except:
            pass

    def on_input_changed(self, e: Input.Changed):
        if e.input.id == 'seed_phrase_len':
            self.log('changing seed_phrase_len', e.value)
            try:
                self.seed_phrase_len = int(e.value)
            except:
                self.log('invalid seed_phrase_len: ', e.value)
            return

        if isinstance(e.input, MnemonicWordInput):
            inputs = self.query(MnemonicWordInput)
            words = [i.value for i in inputs]
            self.words = ' '.join(words)

    def on_paste(self, e: events.Paste):
        # if isinstance(e.sender, MnemonicWordInput):
        e.stop()
        words = e.text.split(' ')
        for word, i in zip(words, self.query(MnemonicWordInput)):
            i.value = word
            i.refresh()

    def try_decode(self) -> bytes:
        raise NotImplementedError()


class BipMnemonicDecoder(MnemonicDecoder, ViewFor[BipMnemonicEncoding]):
    """
    Subclass of MnemonicDecoder that turns a seed phrase + password into the seed following the BIP-39 spec.
    """
    word_list_lang = reactive('english')
    passphrase = reactive('')
    decoder = reactive[BipMnemonicEncoding | None](None)

    def __init__(self, decoder: BipMnemonicEncoding):
        super().__init__()
        decoder.set_lang(self.word_list_lang)
        self.decoder = decoder

    def compose_options(self) -> ComposeResult:
        yield from super().compose_options()
        yield Label('Language')
        yield Input(self.word_list_lang, id='word_list_lang')
        yield Label('Passphrase')
        yield Input(id='seed_passphrase', placeholder='Optional')

    def watch_word_list_lang(self, lang: str):
        if self.decoder is not None:
            self.decoder.set_lang(lang)

    def try_decode(self):
        encoded = MnemonicAndPassphrase(
            ' '.join(self.words),
            self.passphrase)
        return self.decoder.decode(encoded)


class SlipMnemonicDecoder(MnemonicDecoder, ViewFor[SlipMnemonicEncoding]):

    def __init__(self, decoder: SlipMnemonicEncoding):
        self.decoder = decoder
        super().__init__()

    def try_decode(self):
        raise NotImplementedError()


class RawSeedDecoder(Decoder, ViewFor[StringEncoding]):

    def __init__(self, decoder: StringEncoding):
        self.decoder = decoder
        super().__init__()

    def try_decode(self) -> bytes:
        pass
