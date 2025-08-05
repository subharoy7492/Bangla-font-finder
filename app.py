from flask import Flask, request, jsonify, send_from_directory, render_template_string
from PIL import Image
import pytesseract
import os

app = Flask(__name__)
os.makedirs("uploads", exist_ok=True)
os.makedirs("fonts", exist_ok=True)

@app.route("/")
def index():
    return render_template_string(open("index.html").read())

@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    image = request.files["image"]
    path = os.path.join("uploads", image.filename)
    image.save(path)

    text = pytesseract.image_to_string(Image.open(path), lang="ben")
    matched_font = "Harafan" if "অ" in text else "Unknown"

    return jsonify({"font_name": matched_font})

@app.route("/fonts/<filename>")
def fonts(filename):
    return send_from_directory("fonts", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)