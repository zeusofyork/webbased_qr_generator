from flask import Flask, request, send_file, render_template_string
import qrcode
import io

app = Flask(__name__)

# HTML template to display the QR code and download option
qr_display_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code Generator</title>
</head>
<body>
    <h1>QR Code Generator</h1>
    <form action="/generate" method="post">
        <label for="data">Enter text or URL:</label><br>
        <input type="text" id="data" name="data" required><br><br>
        <button type="submit">Generate QR Code</button>
    </form>
    {% if qr_code %}
    <hr>
    <h2>Generated QR Code</h2>
    <img src="data:image/png;base64,{{ qr_code }}" alt="QR Code"><br><br>
    <form action="/download" method="post">
        <input type="hidden" name="data" value="{{ data }}">
        <button type="submit">Download QR Code</button>
    </form>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(qr_display_template)

@app.route("/generate", methods=["POST"])
def generate_qr_code():
    data = request.form.get("data")
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
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    # Convert image to base64 for inline display
    import base64
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

    return render_template_string(qr_display_template, qr_code=img_base64, data=data)

@app.route("/download", methods=["POST"])
def download_qr_code():
    data = request.form.get("data")
    if not data:
        return "<h1>Error: No data provided!</h1>"

    # Generate the QR code again for download
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
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return send_file(
        img_bytes, mimetype="image/png", as_attachment=True, download_name="qr_code.png"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
