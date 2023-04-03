import click
import mnemonic as bip

from keys_r_us import encoding
from keys_r_us.cli import util


@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument('words', required=False)
@click.option('--lang', default='english')
@click.option('--passphrase', default='')
@click.option('-f', '--format', default='hex')
@click.pass_context
def derive(ctx: click.Context,
           words: str | None,
           lang: str,
           passphrase: str,
           format: str):
    """
    Derive the seed from a BIP-0039 mnemonic + passphrase.

    Words must be provided as an argument or via stdin.
    """
    m = bip.Mnemonic(lang)
    enc = encoding.get_encoding(format)
    enc_opts = util.parse_format_options(enc, ctx.args)

    def _derive(mnemonic: str):
        mnemonic = mnemonic.strip()
        if not m.check(mnemonic):
            raise ValueError('invalid mnemonic')
        seed = m.to_seed(mnemonic, passphrase)
        print(encoding.encode(seed, enc, **enc_opts))

    if words is not None:
        _derive(words)
    else:
        stdin = click.get_text_stream('stdin')
        for line in stdin:
            _derive(line)
