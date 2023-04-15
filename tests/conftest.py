import click
import pytest
from click.testing import CliRunner as _CliRunner


class CliRunner(_CliRunner):
    def __init__(self, command: click.Command):
        super().__init__()
        self.command = command

    def __call__(self, *args, stdin=None, **kwargs):
        kwargs.setdefault('catch_exceptions', False)
        return self.invoke(self.command, args, stdin, **kwargs)


@pytest.fixture(scope='session')
def keys_r_us_cli() -> CliRunner:
    from keys_r_us import cli
    return CliRunner(cli.main)
