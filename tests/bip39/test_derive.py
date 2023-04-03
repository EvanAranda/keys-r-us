import pytest


class TestWordsFromStdin:

    @pytest.mark.parametrize('passphrase', ['', 'passphrase'])
    def test_single_line(self, keys_r_us_cli, passphrase: str):
        words = keys_r_us_cli('bip39', 'generate')
        seed = keys_r_us_cli(
            'bip39', 'derive',
            '--passphrase', passphrase,
            '-f', 'hex',
            stdin=words.stdout)

        assert seed.exit_code == 0, seed.exc_info

        # the seed should be 64 bytes long (128 hex characters)
        assert len(seed.stdout.strip()) == 128, seed.exc_info

    @pytest.mark.parametrize('passphrase', ['', 'passphrase'])
    def test_multi_line(self, keys_r_us_cli, passphrase: str):
        mnemonics = '\n'.join(keys_r_us_cli('bip39', 'generate').stdout.strip() for _ in range(3))
        seeds = keys_r_us_cli(
            'bip39', 'derive',
            '--passphrase', passphrase,
            '-f', 'hex',
            stdin=mnemonics)

        assert seeds.exit_code == 0, seeds.exc_info

        seeds = seeds.stdout.strip().split('\n')
        assert len(seeds) == 3
        for seed in seeds:
            assert len(seed.strip()) == 128


class TestWordsFromArgument:

    def test_valid_mnemonic_length(self, keys_r_us_cli):
        words = keys_r_us_cli('bip39', 'generate')
        seed = keys_r_us_cli('bip39', 'derive', words.stdout.strip())
        assert seed.exit_code == 0, seed.exc_info

    def test_invalid_mnemonic_length(self, keys_r_us_cli):
        words = 'hello world'
        with pytest.raises(ValueError):
            seed = keys_r_us_cli('bip39', 'derive', words)
