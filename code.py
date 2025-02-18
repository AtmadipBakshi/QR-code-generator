import qrcode
from flask import Flask, request, render_template
import io
import base64

app = Flask(__name__)

def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    return img

@app.route('/', methods=['GET', 'POST'])
def index():
    img_data = None
    if request.method == 'POST':
        data = request.form['data']
        img = generate_qr(data)
        img_io = io.BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        img_data = f"data:image/png;base64,{img_base64}"
    return render_template('index.html', img_data=img_data)

if __name__ == "__main__":
    app.run(debug=True)
