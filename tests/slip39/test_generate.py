import itertools

import pytest


class TestOutputAsEncodedString:

    @pytest.mark.parametrize('seed_format', ['hex', 'base58'])
    @pytest.mark.parametrize('share_format', ['hex', 'base58', 'qr'])
    @pytest.mark.parametrize('passphrase', ['', 'passphrase'])
    def test_generate_and_recover(self, keys_r_us_cli, tmp_path, seed_format, share_format: str, passphrase: str):
        words = keys_r_us_cli('bip39', 'generate')
        seed = keys_r_us_cli('bip39', 'derive', words.stdout.strip(), '-f', seed_format)

        extra_args = []
        if share_format == 'qr':
            extra_args.extend(('--qr-filename', str(tmp_path / 'share.png')))

        generate_result = keys_r_us_cli(
            'slip39', 'generate',
            seed.stdout.strip(),
            '--seed-format', seed_format,
            '-f', share_format,
            '-p', passphrase,
            *extra_args
        )

        assert generate_result.exit_code == 0, generate_result.exc_info

        shares = generate_result.stdout.strip().splitlines()

        recover_result = keys_r_us_cli(
            'slip39', 'recover',
            *itertools.chain.from_iterable(
                ('-s', f, '-f', share_format)
                for f in shares[:2]
            ),
            '-p', passphrase,
            '-o', seed_format
        )

        assert recover_result.exit_code == 0, recover_result.exc_info
        assert recover_result.stdout.strip() == seed.stdout.strip()
