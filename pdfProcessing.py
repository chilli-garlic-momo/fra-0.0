from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
import pytesseract
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    file = request.files['file']
    pdf_bytes = file.read()
    
    # Convert PDF to images (one per page)
    images = convert_from_bytes(pdf_bytes)
    
    all_text = ""
    for img in images:
        text = pytesseract.image_to_string(img, lang='eng')
        all_text += text + "\n\n"
    
    # TODO: Pass all_text to NER extraction module
    
    # For now, returning raw OCR text
    return jsonify({"ocr_text": all_text})

if __name__ == "__main__":
    app.run(debug=True)
