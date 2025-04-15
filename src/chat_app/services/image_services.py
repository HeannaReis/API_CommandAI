import os
from dotenv import load_dotenv
from google import genai
from PIL import Image
from io import BytesIO

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave da API Gemini do arquivo .env
api_key = os.getenv("API_KEY_GEMINI")

# Verifica se a chave da API foi carregada corretamente
if not api_key:
    raise ValueError("API_KEY_GEMINI não encontrada no arquivo .env")

# Inicializa o Gemini
genai.configure(api_key=api_key)

def generate_image(prompt: str) -> Image.Image | None:
    """
    Gera uma imagem usando o modelo Gemini com base no prompt fornecido.

    Args:
        prompt (str): O prompt de texto para gerar a imagem.

    Returns:
        Image.Image | None: A imagem gerada como um objeto PIL Image ou None em caso de falha.
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
        response = model.generate_content(prompt)
        if response.prompt_feedback:
          print('Reason: {}'.format(response.prompt_feedback.block_reason))
        # Verifique se a resposta contém dados de imagem
        if response.parts:
            for part in response.parts:
                if part.mime_type == 'image/png':
                    return Image.open(BytesIO(part.data))
        print(response.text)
        return None
    except Exception as e:
        print(f"Erro ao gerar imagem: {e}")
        return None

# Exemplo de uso (fora do Streamlit):
if __name__ == "__main__":
    image = generate_image("Desenhe um gato astronauta no espaço sideral, estilo cartoon.")
    if image:
        image.show() # Exibe a imagem (opcional)
        image.save("gato_astronauta.png") # Salva a imagem (opcional)
    else:
        print("Falha ao gerar a imagem.")