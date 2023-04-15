import click

from keys_r_us.cli.bip32 import bip32
from keys_r_us.cli.bip39 import bip39
from keys_r_us.cli.formats import formats
from keys_r_us.cli.slip39 import slip39
from keys_r_us.cli.transcode import transcode


@click.group()
def main():
    """
    keys-r-us
    """


main.add_command(formats)
main.add_command(transcode)
main.add_command(bip39)
main.add_command(bip32)
main.add_command(slip39)
