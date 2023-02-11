from typing import Iterable, TypeVar, Generic
from uuid import uuid4

from textual.app import ComposeResult
from textual.containers import Horizontal, Container
from textual.message import Message, MessageTarget
from textual.widget import Widget
from textual.widgets import Button

TTabItem = TypeVar('TTabItem')


class Tabs(Generic[TTabItem], Widget):
    DEFAULT_CSS = """
    Tabs {
    }
    
    .tab-header {
        height: auto; 
    }
    
    .active-tab {
        background: $accent; 
    }
    """

    class Selected(Generic[TTabItem], Message):
        def __init__(self, sender: MessageTarget, item: TTabItem):
            super().__init__(sender)
            self.spec = item

    def __init__(self, items: Iterable[TTabItem]):
        self._items = items
        self._content_id = 'id' + uuid4().hex
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Horizontal(*(self.compose_headers()), classes='tab-header')
        yield Container(id=self._content_id)

    def compose_headers(self) -> ComposeResult:
        for item in self._items:
            btn = Button(self.compose_header(item))
            setattr(btn, '__tab_item', item)
            yield btn

    def compose_header(self, item: TTabItem) -> str:
        raise NotImplementedError()

    def compose_content(self, item: TTabItem) -> ComposeResult:
        raise NotImplementedError()

    def on_button_pressed(self, e: Button.Pressed):
        if hasattr(e.button, '__tab_item'):
            container = self.get_child_by_id(self._content_id, Container)
            for n in container.children:
                n.remove()
            content = self.compose_content(getattr(e.button, '__tab_item'))
            container.mount(*content)
            e.stop()

            self.query('.tab-header Button').remove_class('active-tab')
            e.button.add_class('active-tab')
