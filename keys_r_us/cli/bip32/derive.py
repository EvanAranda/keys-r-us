import typing as t

import base58
import click
import mnemonic as bip

from keys_r_us import encoding
from keys_r_us.cli import util


@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.option('--words', default=None)
@click.option('--passphrase', default='')
@click.option('--lang', default='english')
@click.option('--seed', default=None)
@click.option('--seed-format', default='hex')
@click.option('--testnet', is_flag=True, default=False)
@click.option('-f', '--format', default='base58')
@click.pass_context
def derive(ctx: click.Context,
           words: t.Optional[str],
           passphrase: str,
           lang: str,
           seed: t.Optional[str],
           seed_format: str,
           testnet: bool,
           format: str):
    """
    Derive the BIP-0032 master key from a BIP-0039 mnemonic + passphrase or seed.
    """
    m = bip.Mnemonic(lang)
    enc = encoding.get_encoding(format)
    enc_opts = util.parse_format_options(enc, ctx.args)

    def _derive(secret: bytes):
        key = base58.b58decode(m.to_hd_master_key(secret, testnet))
        print(encoding.encode(key, format, **enc_opts))

    if words is not None:
        _derive(m.to_seed(words, passphrase))
    elif seed is not None:
        _derive(encoding.get_encoding(seed_format).decode(seed))
    else:
        raise ValueError('either --words or --seed must be provided')
