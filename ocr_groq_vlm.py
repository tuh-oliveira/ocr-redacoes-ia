import base64
import time
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class GroqVLMOCR:
    def __init__(self):
        self.model = "qwen/qwen3.6-27b"
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
                    response = client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": """Transcreva somente a redação presente na imagem.

Copie exatamente o que está escrito. Não corrija, não interprete, não reformule e não complete nada.

Preserve as palavras, erros, acentos, pontuação, maiúsculas/minúsculas, parágrafos e quebras de linha exatamente como aparecem.

IMPORTANTE: respeite o fim de cada linha da imagem. Não junte duas linhas diferentes em uma só linha. Cada linha visual da redação deve permanecer como linha separada no resultado. Se uma linha termina em "à", por exemplo, o texto deve terminar ali e não continuar na mesma linha com a próxima linha da imagem.

Não reagrupe parágrafos, não concatene frases de linhas distintas e não remova quebra de linha por causa do fluxo de leitura.

Ignore cabeçalhos, campos de correção, notas, números de prontuário e outros textos que não façam parte da redação.

Retorne somente o texto da redação, sem explicações, sem análise e sem comentários."""
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{image_base64}"
                                        }
                                    }
                                ],
                            }
                        ],
                        temperature=0.1
                    )

                    if response.choices and len(response.choices) > 0:
                        content = response.choices[0].message.content or ""
                        # Remove blocos de raciocínio interno <think>...</think>
                        content_limpo = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
                        return content_limpo

                    return "Sem texto retornado."

                except Exception as e:
                    if "503" in str(e) or "429" in str(e):
                        time.sleep(2 ** attempt)
                    else:
                        return f"Erro Groq: {str(e)}"

            return "Groq sobrecarregado após várias tentativas."

        except Exception as e:
            return f"Erro geral: {str(e)}"