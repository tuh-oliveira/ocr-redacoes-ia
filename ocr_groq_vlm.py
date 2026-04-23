import base64
import time
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class GroqVLMOCR:
    def __init__(self):
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"
        self.default_api_key = os.getenv("GROQ_API_KEY")

    def extract_image_file(self, image_path, api_key=None):
        try:
            # Usa chave do usuário ou fallback para sua
            key = api_key if api_key else self.default_api_key

            if not key:
                return "Nenhuma API key fornecida."

            client = OpenAI(
                api_key=key,
                base_url="https://api.groq.com/openai/v1"
            )

            with open(image_path, "rb") as f:
                image_bytes = f.read()

            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            max_retries = 3

            for attempt in range(max_retries):
                try:
                    response = client.responses.create(
                        model=self.model,
                        input=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "input_text", "text": "Just extract all the text from the image, and give me the extracted text only as a reply."},
                                    {
                                        "type": "input_image",
                                        "image_url": f"data:image/png;base64,{image_base64}"
                                    }
                                ],
                            }
                        ],
                    )

                    if hasattr(response, "output_text") and response.output_text:
                        return response.output_text

                    return "Sem texto retornado."

                except Exception as e:
                    if "503" in str(e):
                        time.sleep(2 ** attempt)
                    else:
                        return f"Erro Groq: {str(e)}"

            return "Groq sobrecarregado após várias tentativas."

        except Exception as e:
            return f"Erro geral: {str(e)}"