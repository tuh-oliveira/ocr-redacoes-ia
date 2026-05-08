import base64
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def process_image_groq(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.responses.create(
        model="llama-3.2-11b-vision-preview",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": """Extraia todo o texto da imagem.

Regras:
- Preserve acentuação
- Organize em parágrafos
- Corrija erros evidentes
- Não invente conteúdo
"""},

                    {
                        "type": "input_image",
                        "image_base64": image_base64
                    }
                ]
            }
        ]
    )

    texto = response.output[0].content[0].text
    return texto.split("\n")