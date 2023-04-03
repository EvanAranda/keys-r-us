import click

from keys_r_us import encoding
from keys_r_us.cli import util


@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument('secret')
@click.argument('from_format')
@click.argument('to_format')
@click.pass_context
def transcode(ctx: click.Context,
              secret: str,
              from_format: str,
              to_format: str):
    """
    Transcode a secret between different formats.
    """
    print(encoding.encode(
        encoding.decode(secret, from_format),
        to_format,
        **util.parse_format_options(to_format, ctx.args)))
