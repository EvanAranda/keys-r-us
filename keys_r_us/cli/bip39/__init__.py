import click

from keys_r_us.cli.bip39.derive import derive
from keys_r_us.cli.bip39.generate import generate


@click.group()
def bip39():
    """
    BIP-0039
    """


bip39.add_command(generate)
bip39.add_command(derive)
