import typing as t

from keys_r_us import encoding


def parse_format_options(enc: t.Union[str, encoding.SecretEncoder],
                         extra_args: t.Sequence[str]) -> t.Dict[str, t.Any]:
    """
    Parse the format options from the command line arguments.
    """
    extra_args = list(extra_args)
    enc = encoding.get_encoding(enc) if isinstance(enc, str) else enc
    options = {k: v.default for k, v in enc.options.items()}
    arg_prefix = f'--{enc.name}-'
    i = 0
    while i < len(extra_args):
        if extra_args[i].startswith(arg_prefix):
            arg_name = extra_args[i].lstrip(arg_prefix)
            if arg_name not in enc.options:
                continue

            opt = enc.options[arg_name]

            if opt.is_flag:
                options[arg_name] = True
            else:
                options[arg_name] = opt.ctor(extra_args.pop(i + 1))

        i += 1

    return options
