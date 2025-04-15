# src/image_processor.py
import os
import time
import shutil
import json
from config.config import Config
from services.gpt_services import GenerativeModelHandler
from services.document_service import DocumentService
from services.markdown_service import MarkdownService
from utils.file_utils import list_images
from core.logger_config import logger
from core.rate_limiter import RateLimiter

class ImageProcessor:
    def __init__(self, rate_limiter: RateLimiter):
        self.gpt_handler = GenerativeModelHandler("gemini-2.0-flash-exp")
        self.document_service = DocumentService()
        self.markdown_service = MarkdownService()
        os.makedirs(Config.PROCESSED_DIR, exist_ok=True)
        self.prompt = self._load_prompt()
        self.history = []
        self.rate_limiter = rate_limiter
        self.historico_json_file = "historico_analises.json"
        self.analises_anteriores = self._carregar_historico_json()  # Carrega o histórico ao inicializar

    def _load_prompt(self):
        try:
            with open(Config.PROMPT_DOC_FILE, "r", encoding="utf-8") as file:
                prompt = file.read().strip()
                logger.info(f"Prompt carregado com sucesso: {prompt}")
                return prompt
        except FileNotFoundError:
            logger.error(f"Arquivo de prompt não encontrado em {Config.PROMPT_DOC_FILE}")
            raise FileNotFoundError(f"Arquivo de prompt não encontrado em {Config.PROMPT_DOC_FILE}")

    def _carregar_historico_json(self):
        try:
            with open(self.historico_json_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def _salvar_historico_json(self):
        with open(self.historico_json_file, "w") as f:
            json.dump(self.analises_anteriores, f, indent=4)

    def process_images(self):
        images = list_images(Config.ASSETS_DIR)
        if not images:
            logger.warning("Nenhuma imagem encontrada em 'assets/'.")
            return

        for idx, image_name in enumerate(images, start=1):
            logger.info(f"Processando imagem {idx}/{len(images)}: {image_name}")

            try:
                self.rate_limiter.wait_for_slot()
                summary = self._process_image(image_name)
                self.document_service.add_image_summary(image_name, summary)
                self.markdown_service.add_image_summary(image_name, summary)
                self.document_service.save_document()
                self.markdown_service.save_markdown()
                self._move_image(image_name)
                self._update_history(image_name, summary)

                # Não adicionar a mesma informação repetidas vezes
                # self.analises_anteriores.append(f"Imagem: {image_name}, Resumo: {summary}")
                # self._salvar_historico_json()

            except Exception as e:
                logger.error(f"Erro ao processar a imagem {image_name}: {e}", exc_info=True)

            time.sleep(4)
            logger.info("Preparando a próxima análise...")

    def _process_image(self, image_name):
        img_path = os.path.join(Config.ASSETS_DIR, image_name)
        processed_path = os.path.join(Config.PROCESSED_DIR, image_name)
        shutil.copy2(img_path, processed_path)

        try:
            # Não precisa carregar o histórico a cada imagem
            # self._carregar_historico_json()

            historico_str = "\n".join([f"{entry['image_name']}: {entry['summary']}" for entry in self.history])
            prompt_com_historico = f"{self.prompt}\nHistórico:\n{historico_str}\nAnalise a seguinte imagem: {image_name}"
            response_text = self.gpt_handler.generate_content_from_image(img_path, prompt_com_historico)
            logger.info(f"Resumo gerado para '{image_name}': {response_text}")
            return response_text
        except Exception as e:
            logger.error(f"Erro ao processar '{image_name}': {str(e)}")
            return f"Erro ao processar imagem: {str(e)}"

    def _move_image(self, image_name):
        origem = os.path.join(Config.ASSETS_DIR, image_name)
        destino = os.path.join(Config.PROCESSED_DIR, image_name)
        shutil.move(origem, destino)
        logger.info(f"Imagem '{image_name}' movida para '{Config.PROCESSED_DIR}'.")

    def _update_history(self, image_name, summary):
        self.history.append({"image_name": image_name, "summary": summary})
        logger.info(f"Histórico atualizado com '{image_name}'.")

    def get_history(self):
        return self.history