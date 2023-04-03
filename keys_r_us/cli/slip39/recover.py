import struct
import typing as t

import click
import shamir_mnemonic as slip
from shamir_mnemonic import wordlist

from keys_r_us import encoding


def _capture_image() -> bytes:
    return bytes(256 * 256 * 3)


@click.command()
@click.option('-s', '--shares', required=True, multiple=True)
@click.option('-f', '--formats', required=True, multiple=True)
@click.option('-p', '--passphrase', default='')
@click.option('-o', '--output-format', default='hex')
def recover(shares: t.Sequence[str],
            formats: t.Sequence[str],
            passphrase: str,
            output_format: str
            ):
    """
    Recovers a secret that has been split by combining sufficient Shamir shares.
    """
    if len(shares) != len(formats):
        print('invalid input: the format of each share is required.')
        exit(1)

    share_mnemonics: t.List[str] = []

    for s, f in zip(shares, formats):
        secret = encoding.decode(s, f)
        n_indices = len(secret) // 2
        indices = struct.unpack(f'{n_indices}h', secret[:n_indices * 2])
        share_mnemonic = wordlist.mnemonic_from_indices(indices)
        share_mnemonics.append(share_mnemonic)

    secret = slip.combine_mnemonics(share_mnemonics, passphrase.encode())
    print(encoding.encode(secret, output_format))
