import pytest
import os
import sys
import io

# Adiciona o diretório raiz do projeto ao path para achar o app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    # Criar diretórios necessários para teste
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)
    
    with app.test_client() as client:
        yield client

def test_invalid_image_format(client):
    """
    Testa o fluxo: Upload de Imagem -> Inválida -> Tratamento adequado do erro.
    """
    data = {
        "file": (io.BytesIO(b"dummy content"), "test.pdf")
    }
    response = client.post("/", data=data, content_type="multipart/form-data")
    
    # Deve retornar 200 (render_template) e conter a mensagem de erro
    assert response.status_code == 200
    assert b"Formato de imagem inv\xc3\xa1lido" in response.data or b"Formato de imagem" in response.data

def test_no_method_selected(client):
    """
    Testa o fluxo: Pelo menos 1 método selecionado? -> Não -> Exibição de aviso ao usuário.
    """
    data = {
        "file": (io.BytesIO(b"fake image data"), "test.png")
        # Sem 'metodos' no formulário
    }
    response = client.post("/", data=data, content_type="multipart/form-data")
    
    assert response.status_code == 200
    assert b"Selecione ao menos um m\xc3\xa9todo" in response.data or b"Selecione ao menos um" in response.data

def test_groq_failure_isolation(client, monkeypatch):
    """
    Testa o fluxo Backend: Execução simultânea. Se a API Groq falhar,
    exibe erro apenas na seção Groq, sem interromper Tesseract e EasyOCR.
    """
    def mock_easy(*args, **kwargs):
        return ["Texto EasyOCR"]
    
    def mock_tess(*args, **kwargs):
        return ["Texto Tesseract"]
    
    class MockGroqVLMOCR:
        def extract_image_file(self, *args, **kwargs):
            raise Exception("503 Service Unavailable")

    monkeypatch.setattr("app.process_image_easy", mock_easy)
    monkeypatch.setattr("app.process_image_tesseract", mock_tess)
    monkeypatch.setattr("app.groq_ocr", MockGroqVLMOCR())

    data = {
        "file": (io.BytesIO(b"fake image data"), "test.png"),
        "metodos": ["easyocr", "tesseract", "groq"]
    }
    response = client.post("/", data=data, content_type="multipart/form-data")
    
    assert response.status_code == 200
    # EasyOCR e Tesseract devem apresentar os resultados normalmente
    assert b"Texto EasyOCR" in response.data
    assert b"Texto Tesseract" in response.data
    # Groq deve ter tratamento de erro isolado
    assert b"Erro no Groq" in response.data

def test_save_correction(client):
    """
    Testa as Fases 6 e 7 do Diagrama de Sequência:
    Abre editor e altera -> Salva correção -> Cria arquivo .txt -> Retorna status 200 OK
    """
    texto_editado = "Redacao corrigida com sucesso!"
    nome_arquivo = "teste_redacao"
    
    data = {
        "salvar_texto": "1",
        "texto_editado": texto_editado,
        "nome_arquivo": nome_arquivo
    }
    
    response = client.post("/", data=data, content_type="multipart/form-data")
    
    assert response.status_code == 200
    # Verifica se a mensagem de sucesso está na página (flash success)
    assert b"Texto corrigido salvo com sucesso!" in response.data or b"sucesso" in response.data
    
    # Verifica se o arquivo foi realmente criado
    caminho_arquivo = os.path.join("correcoes", f"{nome_arquivo}_corrigido.txt")
    assert os.path.exists(caminho_arquivo)
    
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        conteudo = f.read()
    
    assert conteudo == texto_editado
    
    # Limpeza
    if os.path.exists(caminho_arquivo):
        os.remove(caminho_arquivo)
