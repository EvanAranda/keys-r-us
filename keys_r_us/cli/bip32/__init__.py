import click

from keys_r_us.cli.bip32.derive import derive


@click.group()
def bip32():
    """
    BIP-0032
    """


bip32.add_command(derive)
