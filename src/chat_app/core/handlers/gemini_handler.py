from services.gpt_services import GenerativeModelHandler
from core.logger_config import logger
from core.rate_limiter import RateLimiter  # supondo que você salvou a classe acima em core/rate_limiter.py

class GeminiHandler:
    def __init__(self, model_name):
        self.handler = GenerativeModelHandler(model_name)
        self.rate_limiter = RateLimiter(max_requests=15, period_seconds=60)

    def generate_content(self, img_path, prompt):
        self.rate_limiter.wait_for_slot()  # Aguarda até que haja um slot disponível

        if img_path:
            logger.info(f"Enviando para IA - Imagem: {img_path}, Prompt: {prompt}")
            return self.handler.generate_content_from_image(img_path, prompt)
        else:
            logger.info(f"Enviando para IA - Prompt (sem imagem): {prompt}")
            return self.handler.generate_content_from_text(prompt)