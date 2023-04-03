import click

from keys_r_us import encoding


@click.command()
@click.argument('name', required=False)
@click.option('-s', '--short', is_flag=True, default=False)
def formats(name: str | None, short: bool):
    """
    Display all the output formats and their configuration.
    """
    if short:
        for enc in encoding.formats:
            print(enc.name)
        return

    def print_encoding_info(enc: encoding.SecretEncoder):
        print(f"Format '{enc.name}'")
        print()
        print(enc.desc)
        print()

        if len(enc.options):
            print('Options:')
            for opt_name, opt in enc.options.items():
                print(f'--{enc.name}-{opt_name:10} {opt.description}')

    if name:
        print_encoding_info(encoding.get_encoding(name))
        return

    for i, enc in enumerate(encoding.formats):
        print_encoding_info(enc)
        if i != len(encoding.formats) - 1:
            print('-' * 80)
