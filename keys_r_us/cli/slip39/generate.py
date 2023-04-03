import struct
import typing as t

import click
import shamir_mnemonic as slip
from shamir_mnemonic import wordlist

from keys_r_us import encoding
from keys_r_us.cli import util


@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument('seed', required=True)
@click.option('--seed-format',
              default='hex',
              help='Encoding of the seed string.')
@click.option('-p', '--password',
              default='',
              help='Passphrase used to encrypt the master secret before splitting.')
@click.option('-t', '--group-threshold',
              default=1,
              help='Number of top-level groups required recover the secret.')
@click.option('-g', '--group',
              default=['2:3'],
              help='{Threshold for group}:{Number of members in group}.',
              multiple=True)
@click.option('-f', '--format',
              default='hex',
              help='Name of the output encoding. See formats command.')
@click.pass_context
def generate(ctx: click.Context,
             seed: str,
             seed_format: str,
             password: str,
             group_threshold: int,
             group: t.Sequence[str],
             format: str):
    """
    Split a secret into multiple parts using Shamir's Secret Sharing.
    """
    _split(
        encoding.get_encoding(seed_format).decode(seed),
        password.encode(),
        group_threshold,
        [_parse_group_options(g) for g in group],
        encoding.get_encoding(format),
        util.parse_format_options(format, ctx.args)
    )


def _parse_group_options(group: str) -> t.Tuple[int, int]:
    """
    Parse the group options into a list of (threshold, number of members) tuples.
    """
    th, n = group.split(':')
    th, n = int(th), int(n)
    assert th <= n
    return th, n


def _split(secret: bytes,
           password: bytes,
           group_threshold: int,
           groups: t.Sequence[t.Tuple[int, int]],
           output_encoding: encoding.SecretEncoder,
           output_encoding_opts: dict):
    """
    Encode a secret using the named encoding and output the result to stdout or file.
    """
    mnemonic_groups = slip.generate_mnemonics(
        group_threshold, groups,
        secret, password)

    orig_filename = output_encoding_opts.get('filename')

    for i, mnemonic_group in enumerate(mnemonic_groups, 1):
        for j, mnemonic in enumerate(mnemonic_group, 1):
            indices = wordlist.mnemonic_to_indices(mnemonic)
            value = struct.pack(f'{len(indices)}h', *indices)
            if orig_filename:
                output_encoding_opts['filename'] = orig_filename.with_stem(orig_filename.stem + f'_{i}_{j}')

            print(encoding.encode(
                value,
                output_encoding,
                **output_encoding_opts))
