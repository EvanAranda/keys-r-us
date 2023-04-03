import base64
import typing as t
from pathlib import Path

import PIL.Image
import qrcode
from pyzbar import pyzbar

from .interface import SecretEncoder, Option


class QRSecretEncoder(SecretEncoder):
    """
    Encoding that outputs a secret as a QR code.
    """

    name = 'qr'
    desc = 'QR Code Encoding.'
    options = dict(
        size=Option('Pixels per block of the qr code.', 10, int),
        filename=Option('File to write the qr code to.', Path('./share.png'), Path)
    )

    @classmethod
    def encode(cls, secret: bytes, **opts) -> str:
        output_location = Path(opts['filename']).resolve()
        img_format = output_location.suffix
        if not img_format.startswith('.'):
            raise ValueError(f'invalid image format: {img_format}')
        img_format = img_format.lstrip('.')

        img = qrcode.make(
            base64.b64encode(secret),
            box_size=opts['size'])
        img.save(output_location, kind=img_format)
        return str(output_location)

    @classmethod
    def decode(cls, encoded: t.Any, **opts) -> bytes:
        img = PIL.Image.open(encoded)
        decoded = pyzbar.decode(img, symbols=[pyzbar.ZBarSymbol.QRCODE])
        if not decoded or len(decoded) != 1:
            raise RuntimeError(f'did not detect a qr code.')
        return base64.b64decode(decoded[0].data)
