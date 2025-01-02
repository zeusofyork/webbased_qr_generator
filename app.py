from flask import Flask, request, send_file, jsonify
import qrcode
import io

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>QR Code Generator</h1>
    <form action="/generate" method="post">
        <label for="data">Enter text or URL:</label><br>
        <input type="text" id="data" name="data" required><br><br>
        <button type="submit">Generate QR Code</button>
    </form>
    """

@app.route('/generate', methods=['POST'])
def generate_qr_code():
    try:
        # Get the input data from the form
        data = request.form.get('data')
        if not data:
            return "<h1>Error: No data provided!</h1>"

        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Create an image from the QR Code instance
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image to a BytesIO object
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        return send_file(img_bytes, mimetype='image/png', as_attachment=True, download_name='qr_code.png')
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
