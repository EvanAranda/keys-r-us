import click

from keys_r_us.cli.bip32 import bip32
from keys_r_us.cli.bip39 import bip39
from keys_r_us.cli.formats import formats
from keys_r_us.cli.slip39 import slip39
from keys_r_us.cli.transcode import transcode


@click.group()
def entry():
    """
    keys-r-us
    """


entry.add_command(formats)
entry.add_command(transcode)
entry.add_command(bip39)
entry.add_command(bip32)
entry.add_command(slip39)
