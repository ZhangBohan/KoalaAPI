import qrcode
from StringIO import StringIO
from flask import send_file, request

from . import api_v1


@api_v1.route('/qrcode', methods=['GET', 'POST'])
def v1_qrcode():
    box_size_arg = 'box_size'
    border_arg = 'border'
    box_size = request.args.get(box_size_arg, 10)
    border = request.args.get(border_arg, 1)
    url = request.args.get('url')

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    if request.method == 'GET':
        data = {}
        if url:
            data = url
        else:
            for key, value in request.args.items():
                if key != border_arg and key != border_arg and key != url:
                    data[key] = value[0]
        qr.add_data(data)
    else:
        qr.add_data(request.data)
    qr.make(fit=True)

    img = qr.make_image()
    return _serve_pil_image(img)


def _serve_pil_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png', cache_timeout=0)
