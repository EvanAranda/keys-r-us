from typing import TypeVar, Generic

from di_ioc import AbstractServiceProvider
from textual.widget import Widget

TViewModel = TypeVar('TViewModel')


class ViewFor(Generic[TViewModel], Widget):
    pass


def app_services(obj) -> AbstractServiceProvider:
    from keys_r_us.app.main import App

    """
    Helper method to get the service provider from any widget mounted under
    the app.
    :param obj:
    :return:
    """
    if isinstance(obj, App):
        return obj.services

    if isinstance(obj, Widget):
        return app_services(obj.app)

    raise RuntimeError('app services are not accessible from this object.')

