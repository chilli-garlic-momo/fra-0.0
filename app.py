import os
import uuid
from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
import pytesseract
import spacy
from db import save_record  # Updated to use Supabase

app = Flask(__name__)

nlp = spacy.load("fra_ner_model")  # Your trained custom NER model here

def extract_entities(text):
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        label = ent.label_
        entities.setdefault(label, []).append(ent.text)
    return entities

@app.route('/upload', methods=['POST'])
def upload_pdf():
    file = request.files['file']
    pdf_bytes = file.read()

    os.makedirs("uploads", exist_ok=True)
    pdf_path = f"uploads/{uuid.uuid4()}.pdf"
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)

    images = convert_from_bytes(pdf_bytes)
    all_text = ""
    for img in images:
        text = pytesseract.image_to_string(img, lang='eng')
        all_text += text + "\n\n"

    entities = extract_entities(all_text)

    save_record(entities, all_text, pdf_path)

    return jsonify({"status": "success", "entities": entities})

if __name__ == "__main__":
    app.run(debug=True)
