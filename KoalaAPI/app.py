import qrcode
from StringIO import StringIO
from flask import Flask, send_file, request

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/v1/qrcode', methods=['POST'])
def v1_qrcode():
    box_size = request.args.get('box_size', 10)
    border = request.args.get('border', 4)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(request.data)
    qr.make(fit=True)

    img = qr.make_image()
    return _serve_pil_image(img)


def _serve_pil_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


if __name__ == "__main__":
    app.run(debug=True)
