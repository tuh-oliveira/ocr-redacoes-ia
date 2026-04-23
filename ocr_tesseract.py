import pytesseract
import cv2

# AJUSTA ESSE CAMINHO SE PRECISAR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def process_image_tesseract(path):
    try:
        img = cv2.imread(path)

        # Redimensionamento
        h, w = img.shape[:2]
        if w > 1500:
            scale = 1500 / w
            img = cv2.resize(img, (int(w*scale), int(h*scale)))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(gray, lang='por+eng')

        linhas = [l for l in text.split("\n") if l.strip()]
        return linhas

    except Exception as e:
        return [f"Erro Tesseract: {str(e)}"]