from flask import Flask, render_template, request, flash
import os
from datetime import datetime

# OCRs
from ocr_easy import process_image_easy
from ocr_tesseract import process_image_tesseract
from ocr_groq_vlm import GroqVLMOCR

app = Flask(__name__)
app.secret_key = "ocr_redacoes_secret"

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

groq_ocr = GroqVLMOCR()

@app.route("/", methods=["GET", "POST"])
def index():
    resultado_easy = []
    resultado_tess = []
    resultado_groq = []

    texto_editado = ""

    if request.method == "POST":
        file = request.files.get("file")
        api_key_user = request.form.get("api_key")
        metodos = request.form.getlist("metodos")

        # 👇 NOVO: pegar texto editado
        texto_editado = request.form.get("texto_editado")

        # 👇 NOVO: salvar texto corrigido
        if request.form.get("salvar_texto") and texto_editado:
            texto_editado = request.form.get("texto_editado")
            nome_arquivo = request.form.get("nome_arquivo", "texto_corrigido")

            os.makedirs("correcoes", exist_ok=True)

            caminho = os.path.join(
                "correcoes",
                f"{nome_arquivo}_corrigido.txt"
            )

            try:
                with open(caminho, "w", encoding="utf-8") as f:
                    f.write(texto_editado)

                flash("✅ Texto corrigido salvo com sucesso!", "success")

            except Exception as e:
                flash(f"❌ Erro ao salvar: {str(e)}", "error")

        if file:
            path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(path)

            if not metodos:
                return render_template(
                    "index.html",
                    easy=["⚠️ Selecione ao menos um método"],
                    tess=[],
                    groq=[],
                    texto_editado=""
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

            # GROQ
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
        groq=resultado_groq,
        texto_editado=texto_editado
    )

if __name__ == "__main__":
    app.run(debug=True)