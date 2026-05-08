# 📝 OCR de Redações com IA

Sistema desenvolvido para extração e processamento de textos a partir de imagens de redações, utilizando técnicas de OCR tradicional e Inteligência Artificial.

Projeto acadêmico desenvolvido no **IFSP – Câmpus Jacareí**, no curso de Análise e Desenvolvimento de Sistemas.

---

## 🚀 Funcionalidades

* 📷 Upload de imagens
* 🔍 Extração de texto com:

  * Tesseract OCR
  * EasyOCR
* 🤖 Extração com IA multimodal (Groq)
* 📊 Comparação entre diferentes métodos
* 🧠 Organização automática do texto em linhas
* 📈 Avaliação de similaridade entre resultados

---

## 🧠 Tecnologias utilizadas

* Python
* Flask
* EasyOCR
* Tesseract OCR
* OpenCV
* GroqCloud (API compatível com OpenAI)
* Transformers (TrOCR)

---

## 📊 Comparação de desempenho

| Ferramenta | Tipo de Texto | Precisão | Observações                  |
| ---------- | ------------- | -------- | ---------------------------- |
| Tesseract  | Digitado      | ~99%     | Excelente para textos limpos |
| Tesseract  | Manuscrito    | <10%     | Baixo desempenho             |
| EasyOCR    | Manuscrito    | ~45%     | Perde contexto               |
| TrOCR      | Manuscrito    | Variável | Melhor em trechos curtos     |
| Groq VLM   | Digitado      | ~98%     | Muito consistente            |
| Groq VLM   | Manuscrito    | ~85–90%  | Melhor resultado geral       |

---

## ⚙️ Instalação

### 1. Clone o projeto

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

---

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Instale o Tesseract (OBRIGATÓRIO)

Baixe e instale:

👉 https://github.com/UB-Mannheim/tesseract/wiki

Adicione ao PATH:

```
C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

### 5. Configure a API da Groq

Copie o arquivo `.env.example` para `.env` e preencha com sua chave de API:

```bash
copy .env.example .env
```

Em `.env`, deixe apenas sua chave:

```env
GROQ_API_KEY=sua_chave_groq_aqui
```

Obtenha sua chave da API Groq em: https://console.groq.com/

---

## ▶️ Como executar

```bash
python app.py
```

Acesse no navegador:

```
http://127.0.0.1:5000
```

---

## 🧪 Como funciona

O sistema utiliza um pipeline composto por:

1. 📍 Detecção de texto (EasyOCR)
2. 🧩 Agrupamento em linhas
3. 🔤 OCR tradicional (Tesseract / EasyOCR)
4. 🤖 OCR com IA (Groq VLM)
5. 📊 Comparação de resultados

---

## ⚠️ Limitações

* OCR manuscrito ainda apresenta erros
* Dependência de APIs externas (Groq)
* Instabilidade de modelos multimodais
* Resultados variam com qualidade da imagem

---

## 🔮 Possíveis melhorias

* Treinamento de modelo próprio
* Integração com correção automática de redação
* Avaliação estilo ENEM
* Melhor segmentação de texto
* Uso de modelos multimodais mais avançados

---

## 👨‍💻 Autor

**Arthur Araújo de Oliveira**
IFSP – Câmpus Jacareí
Análise e Desenvolvimento de Sistemas

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos.
