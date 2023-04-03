import random

import pytest

from keys_r_us import encoding

_secrets = [
    b'hello world',
    random.randbytes(10)
]


@pytest.mark.parametrize('secret', _secrets)
def test_write_read_loop(tmp_path, secret: bytes):
    img_file = encoding.encode(secret, 'qr', filename=tmp_path / 'test.png')
    decoded = encoding.decode(img_file, 'qr')
    assert decoded == secret
