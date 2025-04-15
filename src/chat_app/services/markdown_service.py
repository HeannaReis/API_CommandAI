import os
from config.config import Config

class MarkdownService:
    def __init__(self):
        self.content = []

    def add_image_summary(self, image_name, summary):
        """Adiciona uma nova imagem e resumo ao conteúdo do Markdown."""
        image_path = f"/processed_images/{image_name}"  # Caminho relativo
        markdown_entry = f"## Imagem: {image_name}\n![{image_name}]({image_path})\n\n{summary}\n"
        self.content.append(markdown_entry)

    def save_markdown(self):
        """Salva os resumos no arquivo Markdown, garantindo que o novo conteúdo seja anexado sem sobrescrever."""
        if not os.path.exists(Config.OUTPUT_MD):  # Se o arquivo não existir, cria o cabeçalho
            with open(Config.OUTPUT_MD, 'w', encoding='utf-8') as f:
                f.write("# Resumo das Análises das Imagens\n\n")

        with open(Config.OUTPUT_MD, 'a', encoding='utf-8') as f:  # Modo 'a' (append)
            f.write("\n".join(self.content) + "\n")  # Adiciona novas entradas

        self.content = []  # Limpa a lista após salvar para evitar duplicação
