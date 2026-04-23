import cv2
import easyocr
from PIL import Image
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

reader = easyocr.Reader(['pt'])

processor = TrOCRProcessor.from_pretrained("microsoft/trocr-large-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-large-handwritten")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def process_image(path):
    img = cv2.imread(path)

    results = reader.readtext(img)

    linhas = []

    for (bbox, text, conf) in results:
        if conf < 0.3:
            continue

        y = bbox[0][1]
        colocado = False

        for linha in linhas:
            if abs(linha["y"] - y) < 25:
                linha["boxes"].append(bbox)
                colocado = True
                break

        if not colocado:
            linhas.append({"y": y, "boxes": [bbox]})

    linhas = sorted(linhas, key=lambda x: x["y"])

    saida = []

    for linha in linhas:
        boxes = linha["boxes"]

        x_min = int(min([p[0] for b in boxes for p in b]))
        x_max = int(max([p[0] for b in boxes for p in b]))
        y_min = int(min([p[1] for b in boxes for p in b]))
        y_max = int(max([p[1] for b in boxes for p in b]))

        crop = img[y_min:y_max, x_min:x_max]

        if crop is None or crop.size == 0:
            continue

        if len(crop.shape) == 3:
            crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        crop = cv2.GaussianBlur(crop, (3, 3), 0)
        crop = cv2.resize(crop, None, fx=2.5, fy=2.5)

        pil_img = Image.fromarray(crop)

        pixel_values = processor(images=pil_img, return_tensors="pt").pixel_values.to(device)

        ids = model.generate(pixel_values, max_new_tokens=100)
        texto = processor.batch_decode(ids, skip_special_tokens=True)[0]

        saida.append(texto)

    return saida