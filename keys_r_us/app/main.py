from di_ioc import AbstractServiceProvider
from textual.app import App as AppBase, ComposeResult
from textual.widgets import Header, Footer

from .services import AppServices
from .spec import SpecSelector


class App(AppBase):
    CSS = """
    Button {
        width: 16;
    } 
    """

    def __init__(self, services: AbstractServiceProvider):
        super().__init__()
        self.services = services

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield self.services.get_required_service(SpecSelector)


def run():
    app = App(AppServices())
    app.run()
