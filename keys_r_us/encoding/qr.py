import base64
import typing as t
from pathlib import Path

import PIL.Image
import qrcode
from pyzbar import pyzbar
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, SquareModuleDrawer

from .interface import SecretEncoder, Option


class QRSecretEncoder(SecretEncoder):
    """
    Encoding that outputs a secret as a QR code.
    """

    name = 'qr'
    desc = 'QR Code Encoding.'
    options = dict(
        size=Option('Pixels per block of the qr code.', 10, int),
        filename=Option('File to write the qr code to.', Path('./share.png'), Path),
        style=Option('Style of the qr code modules (square, rounded).', 'square', str),
    )

    @classmethod
    def encode(cls, secret: bytes, **opts) -> str:
        output_location = Path(opts['filename']).resolve()
        img_format = output_location.suffix
        if not img_format.startswith('.'):
            raise ValueError(f'invalid image format: {img_format}')
        img_format = img_format.lstrip('.')

        match opts['style']:
            case 'square':
                img_factory = StyledPilImage
                module_drawer = SquareModuleDrawer()
            case 'rounded':
                img_factory = StyledPilImage
                module_drawer = RoundedModuleDrawer()
            case _:
                raise ValueError(f'invalid qr code style: {opts["style"]}')

        qr = qrcode.QRCode(
            box_size=opts['size'])
        qr.add_data(base64.b64encode(secret))
        img = qr.make_image(
            image_factory=img_factory,
            module_drawer=module_drawer)
        img.save(output_location, kind=img_format)
        return str(output_location)

    @classmethod
    def decode(cls, encoded: t.Any, **opts) -> bytes:
        img = PIL.Image.open(encoded)
        decoded = pyzbar.decode(img, symbols=[pyzbar.ZBarSymbol.QRCODE])
        if not decoded or len(decoded) != 1:
            raise RuntimeError(f'did not detect a qr code.')
        return base64.b64decode(decoded[0].data)
