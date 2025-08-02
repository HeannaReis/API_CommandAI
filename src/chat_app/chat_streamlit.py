import streamlit as st
import time
from datetime import datetime
from core.handlers.gemini_handler import GeminiHandler
from PIL import Image
import os
import io
from config.config import Config
from core.rate_limiter import RateLimiter
from google import genai
from google.genai import types
from dotenv import load_dotenv
from services.search_files import ler_arquivos_por_extensao


# Carrega as variáveis de ambiente
load_dotenv()

# Inicializa RateLimiter
rate_limiter = RateLimiter(max_requests=7, period_seconds=60)

# Inicializa estados do session_state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "clipboard_image_preview" not in st.session_state:
    st.session_state.clipboard_image_preview = None
if "clipboard_image_file" not in st.session_state:
    st.session_state.clipboard_image_file = None
if "last_message_time" not in st.session_state:
    st.session_state.last_message_time = 0
if "file_uploader_key" not in st.session_state:
    st.session_state.file_uploader_key = "uploader_0"
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None
if "image_prompt" not in st.session_state:
    st.session_state.image_prompt = None

# Limite máximo de mensagens no histórico
MAX_MESSAGES = 10

# Função para carregar o prompt do chat
def load_chat_prompt():
    try:
        with open(Config.PROMPT_CHAT_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Você é um assistente de IA versátil e útil. Você pode conversar sobre diversos assuntos e também analisar imagens quando elas forem fornecidas."

# Adicione o conteúdo dos arquivos Python como contexto
linguagens_suportadas = ['.java'] # <--- Defina as extensões desejadas aqui
codigo_fonte = ler_arquivos_por_extensao(linguagens_suportadas) # <--- Chamada da função alterada
chat_prompt = f"{load_chat_prompt()}\n\nContexto:\n\n{codigo_fonte}"

# Inicializa GeminiHandler
@st.cache_resource
def get_gemini_handler():
    return GeminiHandler("gemini-2.5-flash")

gemini_handler = get_gemini_handler()

# Função para verificar e processar a área de transferência
def check_clipboard():
    try:
        from PIL import ImageGrab

        # Tenta pegar imagem da área de transferência
        img = ImageGrab.grabclipboard()

        if img is not None and isinstance(img, Image.Image):
            # Converte a imagem para bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

            # Cria um objeto similar ao retornado pelo st.file_uploader
            class ClipboardFile:
                def __init__(self, bytes_data):
                    self.bytes_data = bytes_data
                    self.name = f"clipboard_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"

                def getbuffer(self):
                    return self.bytes_data.getvalue()

            return ClipboardFile(img_byte_arr), img
        return None, None
    except Exception as e:
        st.sidebar.error(f"Erro ao acessar a área de transferência: {e}")
        return None, None

# Função para resetar o uploader alterando sua chave
def reset_uploader():
    # Extrai o número da chave atual
    current_key = st.session_state.file_uploader_key
    key_num = int(current_key.split("_")[1])
    # Gera uma nova chave incrementando o número
    st.session_state.file_uploader_key = f"uploader_{key_num + 1}"
    # Limpa o estado do uploaded_image
    st.session_state.uploaded_image = None

# Função que processa a mensagem (com ou sem imagem)
def process_message(user_input, image_data=None, generated_image=None):
    # Marca como processando para bloquear novos inputs
    st.session_state.processing = True
    st.session_state.current_prompt = user_input
    st.session_state.current_image = image_data
    st.session_state.current_generated_image = generated_image

    # Força a reexecução para atualizar a UI e mostrar o indicador de processamento
    st.rerun()

def execute_processing():
    user_input = st.session_state.current_prompt
    image_data = st.session_state.current_image
    generated_image = st.session_state.current_generated_image

    # Garante que não exceda o limite de requisições
    rate_limiter.wait_for_slot()  # Espera até que um slot esteja disponível

    # Continua com o processamento normal
    current_time = time.time()
    time_since_last_message = current_time - st.session_state.last_message_time
    wait_time = max(0, 2 - time_since_last_message)
    time.sleep(wait_time)

    st.session_state.last_message_time = time.time()

    img_path = None
    img_display = None

    # Adiciona mensagem do usuário ao histórico
    if image_data:
        os.makedirs(Config.ASSETS_DIR, exist_ok=True)
        img_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{image_data.name}"
        img_path = os.path.join(Config.ASSETS_DIR, img_name)
        with open(img_path, "wb") as f:
            f.write(image_data.getbuffer())
        with Image.open(img_path) as img:
            img_display = img.copy()

        st.session_state.messages.append({"role": "user", "content": user_input, "image": img_display})
    elif generated_image:
        st.session_state.messages.append({"role": "user", "content": user_input, "image": generated_image})
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})

    # Garante que o histórico não exceda o limite
    if len(st.session_state.messages) > MAX_MESSAGES:
        st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]

    # Constrói o prompt completo incluindo o histórico do chat
    full_prompt = chat_prompt + "\n\n"  # Start with the base prompt

    for message in st.session_state.messages[:-1]: # Exclude the last user message
        role = message["role"]
        content = message["content"]
        full_prompt += f"{role.capitalize()}: {content}\n"

    full_prompt += f"User: {user_input}" # Add current user message

    # Processa resposta da IA
    try:
        if img_path:
            # Se tem imagem: usa o prompt específico para imagens
            response = gemini_handler.generate_content(img_path, full_prompt)
        elif generated_image:
             # Salvando a imagem gerada para ser lida pelo GeminiHandler
             os.makedirs(Config.ASSETS_DIR, exist_ok=True)
             img_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_generated_image.png"
             img_path = os.path.join(Config.ASSETS_DIR, img_name)
             generated_image.save(img_path)

             response = gemini_handler.generate_content(img_path, full_prompt)
        else:
            # Se não tem imagem: apenas conversa normal
            response = gemini_handler.generate_content(None, full_prompt)
    except Exception as e:
        response = f"❌ Erro ao gerar resposta: {str(e)}"

    # Adiciona resposta ao histórico
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Garante que o histórico não exceda o limite
    if len(st.session_state.messages) > MAX_MESSAGES:
        st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]

    # Remove imagem temporária do disco após uso
    if img_path and os.path.exists(img_path):
        os.remove(img_path)

    # Marca o processamento como concluído, mas NÃO limpa as imagens
    st.session_state.processing = False
    st.session_state.current_prompt = None
    st.session_state.current_image = None
    st.session_state.current_generated_image = None

# Callback quando o botão de colar da área de transferência é clicado
def on_paste_click():
    clipboard_file, clipboard_preview = check_clipboard()
    if clipboard_file and clipboard_preview:
        # Reseta o uploader para limpar o arquivo atual
        reset_uploader()
        # Define as imagens da área de transferência
        st.session_state.clipboard_image_file = clipboard_file
        st.session_state.clipboard_image_preview = clipboard_preview
        return True
    return False

# Callback quando um arquivo é carregado
def on_file_upload():
    # Limpa qualquer imagem da área de transferência
    st.session_state.clipboard_image_preview = None
    st.session_state.clipboard_image_file = None

# Callback para limpar todas as imagens
def clear_all_images():
    reset_uploader()
    st.session_state.clipboard_image_preview = None
    st.session_state.clipboard_image_file = None

# Função para gerar imagem com Gemini
def generate_image(prompt):
    # Verifica se a chave da API foi carregada corretamente
    api_key = os.getenv("API_KEY_GEMINI")

    if not api_key:
        raise ValueError("API_KEY_GEMINI não encontrada no arquivo .env")

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp-image-generation',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['Text', 'Image']
            )
        )

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                image = Image.open(io.BytesIO(part.inline_data.data))
                st.session_state.generated_image = image
                return image

    except Exception as e:
        st.error(f"Erro ao gerar imagem: {e}")
        return None

# Executa o processamento se estiver na fila
if st.session_state.processing and hasattr(st.session_state, 'current_prompt'):
    execute_processing()
    st.rerun()

# Configuração da barra lateral
with st.sidebar:
    st.title("Chat IA Java")

    # Seção de geração de imagem
    st.markdown("### Gerar Imagem")
    image_prompt = st.text_input("Digite o prompt para gerar uma imagem:", key="image_prompt")
    if st.button("Gerar Imagem"):
        if image_prompt:
            generated_image = generate_image(image_prompt)

            if generated_image:
                st.session_state.messages.append({"role": "assistant", "image": generated_image, "content": f"Imagem gerada com o prompt: {image_prompt}"})
                st.session_state.generated_image = None #Limpa para não exibir em cima

                st.rerun()
        else:
            st.warning("Por favor, digite um prompt para gerar a imagem.")

    # Seção de imagens (sempre visível)
    st.markdown("### Adicionar Imagem (Opcional)")
    st.caption("Adicione uma imagem se quiser fazer perguntas sobre ela")

    # Layout em duas colunas para os botões de imagem
    col1, col2 = st.columns(2)

    with col1:
        # Botão para verificar a área de transferência
        if st.button("📋 Colar", use_container_width=True):
            if on_paste_click():
                st.success("Imagem colada!")
                st.rerun()
            else:
                st.warning("Nada encontrado.")

    with col2:
        # Botão para limpar a imagem atual (se houver)
        if st.session_state.clipboard_image_preview or st.session_state.uploaded_image:
            if st.button("🗑️ Limpar", use_container_width=True):
                clear_all_images()
                st.rerun()
        else:
            # Placeholder para manter o layout alinhado
            st.write("")

    # Uploader de imagem com chave dinâmica
    uploaded_file = st.file_uploader(
        "📷 Ou faça upload de imagem",
        type=["png", "jpg", "jpeg"],
        label_visibility="visible",
        key=st.session_state.file_uploader_key
    )

    # Atualiza o estado da imagem quando um arquivo é carregado
    if uploaded_file:
        st.session_state.uploaded_image = uploaded_file
        on_file_upload()
        st.success("Imagem carregada!")

    # Exibe a imagem selecionada na barra lateral
    if st.session_state.clipboard_image_preview:
        st.image(st.session_state.clipboard_image_preview, use_container_width=True)
        st.caption("Imagem da área de transferência")
    elif st.session_state.uploaded_image:
        st.image(st.session_state.uploaded_image, use_container_width=True)
        st.caption("Imagem carregada")

    st.markdown("---")

    # Botão para limpar o histórico de conversa
    if st.button("🧹 Limpar conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Desenvolvido com Streamlit e Gemini AI")

# Removendo a exibição da imagem gerada aqui (ela será exibida no histórico de mensagens)
#if st.session_state.generated_image:
#    st.image(st.session_state.generated_image, caption="Imagem Gerada", use_column_width=True)

# Exibição do histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Se houver imagem, exiba-a (se armazenada)
        if message.get("image"):
            st.image(message["image"], use_container_width=True)
        # Exibe o conteúdo da mensagem (texto)
        st.markdown(message["content"])

# Adiciona indicador de digitação quando estiver processando
if st.session_state.processing:
    with st.chat_message("assistant"):
        st.markdown("Gerando resposta...")

# Input de texto - deixe-o como último elemento para manter o comportamento "fixo" natural
if not st.session_state.processing:
    # Verifica se há uma imagem disponível
    current_image = st.session_state.clipboard_image_file or st.session_state.uploaded_image

    # Adapta o placeholder com base na presença de imagem
    if current_image:
        placeholder = "Digite sua pergunta sobre a imagem ou qualquer outro assunto..."
    else:
        placeholder = "Digite sua mensagem..."

    user_input = st.chat_input(placeholder)

    if user_input:
        # Processa a mensagem com a imagem (se houver) ou apenas texto
        process_message(user_input, current_image)
else:
    st.chat_input("Aguarde o processamento...", disabled=True)