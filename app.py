from flask import Flask, render_template, request
import os

# OCRs
from ocr_easy import process_image_easy
from ocr_tesseract import process_image_tesseract
from ocr_groq_vlm import GroqVLMOCR

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

groq_ocr = GroqVLMOCR()

@app.route("/", methods=["GET", "POST"])
def index():
    resultado_easy = []
    resultado_tess = []
    resultado_groq = []

    if request.method == "POST":
        file = request.files.get("file")
        api_key_user = request.form.get("api_key")
        metodos = request.form.getlist("metodos")  # 👈 pega os checkboxes

        if file:
            path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(path)

            # Se não selecionar nada → evita erro
            if not metodos:
                return render_template(
                    "index.html",
                    easy=["⚠️ Selecione ao menos um método"],
                    tess=[],
                    groq=[]
                )

            # EASY OCR
            if "easyocr" in metodos:
                try:
                    resultado_easy = process_image_easy(path)
                except Exception as e:
                    resultado_easy = [f"Erro: {str(e)}"]

            # TESSERACT
            if "tesseract" in metodos:
                try:
                    resultado_tess = process_image_tesseract(path)
                except Exception as e:
                    resultado_tess = [f"Erro: {str(e)}"]

            # GROQ VLM
            if "groq" in metodos:
                try:
                    texto_groq = groq_ocr.extract_image_file(path, api_key_user)
                    resultado_groq = texto_groq.split("\n")
                except Exception as e:
                    resultado_groq = [f"Erro no Groq: {str(e)}"]

    return render_template(
        "index.html",
        easy=resultado_easy,
        tess=resultado_tess,
        groq=resultado_groq
    )

if __name__ == "__main__":
    app.run(debug=True)