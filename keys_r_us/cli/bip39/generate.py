import click
import mnemonic as bip


@click.command()
@click.argument('strength', type=click.INT, default=128)
@click.option('--lang', default='english')
def generate(strength: int, lang: str):
    """
    Generate a BIP-0039 mnemonic or seed.
    """
    m = bip.Mnemonic(lang)
    print(m.generate(strength))
