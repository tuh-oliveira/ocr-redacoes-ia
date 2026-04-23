import easyocr
import cv2

reader = easyocr.Reader(['pt', 'en'], gpu=False)

def process_image_easy(path):
    try:
        img = cv2.imread(path)

        # Redimensiona (evita travar)
        h, w = img.shape[:2]
        if w > 1500:
            scale = 1500 / w
            img = cv2.resize(img, (int(w*scale), int(h*scale)))

        results = reader.readtext(img)

        # 🔥 AGRUPAMENTO POR LINHA
        linhas = []

        for (box, text, conf) in results:
            y = box[0][1]  # pega altura da palavra

            colocado = False

            for linha in linhas:
                # se estiver próximo verticalmente → mesma linha
                if abs(linha["y"] - y) < 20:
                    linha["palavras"].append((box[0][0], text))
                    colocado = True
                    break

            if not colocado:
                linhas.append({
                    "y": y,
                    "palavras": [(box[0][0], text)]
                })

        # 🔥 ordenar linhas (de cima pra baixo)
        linhas = sorted(linhas, key=lambda x: x["y"])

        resultado_final = []

        for linha in linhas:
            # ordenar palavras da esquerda pra direita
            palavras_ordenadas = sorted(linha["palavras"], key=lambda x: x[0])

            frase = " ".join([p[1] for p in palavras_ordenadas])
            resultado_final.append(frase)

        return resultado_final

    except Exception as e:
        return [f"Erro EasyOCR: {str(e)}"]