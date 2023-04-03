import click

from keys_r_us.cli.slip39.generate import generate
from keys_r_us.cli.slip39.recover import recover


@click.group()
def slip39():
    """
    SLIP-0039
    """


slip39.add_command(recover)
slip39.add_command(generate)
