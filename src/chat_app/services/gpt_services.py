# services/gpt_services.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional
import logging
from core.logger_config import logger

class GenerativeModelHandler:
    def __init__(self, model_name: str):
        self.model_name: str = model_name
        self.model: Optional[genai.GenerativeModel] = None
        self.api_key: Optional[str] = None
        self._load_env_variables()
        self._configure_api()
        self._initialize_model()

    def _load_env_variables(self) -> None:
        load_dotenv()
        self.api_key = os.getenv('API_KEY_GEMINI')
        if not self.api_key:
            logger.error("API Key não encontrada nas variáveis de ambiente")
            raise ValueError("API Key não encontrada nas variáveis de ambiente")

    def _configure_api(self) -> None:
        genai.configure(api_key=self.api_key)

    def _initialize_model(self) -> None:
        try:
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"Modelo Gemini '{self.model_name}' inicializado com sucesso.")
        except Exception as e:  
            logger.error(f"Erro ao inicializar o modelo: {e}")
            raise RuntimeError(f"Erro ao inicializar o modelo: {e}")

    def generate_content_from_image(self, image_path: str, prompt: str) -> str:
        try:
            with open(image_path, "rb") as image_file:
                image_bytes = image_file.read()

            response = self.model.generate_content([
                {"mime_type": "image/png", "data": image_bytes},
                prompt
            ])

            logger.info(f"Resposta da IA (imagem): {response.text}")
            return response.text
        except Exception as e:
            logger.error(f"Erro ao processar a imagem: {e}")
            raise RuntimeError(f"Erro ao processar a imagem: {e}")

    def generate_content_from_text(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            logger.info(f"Resposta da IA (texto): {response.text}")
            return response.text
        except Exception as e:
            logger.error(f"Erro ao gerar conteúdo: {e}")
            raise RuntimeError(f"Erro ao gerar conteúdo: {e}")