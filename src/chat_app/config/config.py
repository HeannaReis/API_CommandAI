# src/config.py
import os
from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    print(f"Base Directory: {BASE_DIR}")

    ASSETS_DIR = BASE_DIR.parent / "assets"

    IMAGE_GENERATED_DIR = ASSETS_DIR / "image_generated"
    PROCESSED_DIR = BASE_DIR.parent / "processed_images"
    print(PROCESSED_DIR)
    OUTPUT_DOCX = BASE_DIR / "resumo_analises_imagens.docx"
    OUTPUT_MD = BASE_DIR / "resumo_analises_imagens.md"
    
    # Caminhos para prompts dinâmicos
    PROMPT_DIR = BASE_DIR / "prompt"
    PROMPT_DOC_FILE = PROMPT_DIR / "prompt_doc.txt"
    PROMPT_CHAT_FILE = PROMPT_DIR / "prompt_chat.txt"
    
    # Configuração de logs
    LOG_DIR = BASE_DIR / "logs"
    
    # Configuração de histórico
    HISTORY_FILE = BASE_DIR / "historico_analises.json"
    
    # Configuração de rate limiting
    CHAT_RATE_LIMIT = {"max_requests": 9, "period_seconds": 60}
    API_RATE_LIMIT = {"max_requests": 14, "period_seconds": 60}
    
    @classmethod
    def ensure_directories(cls):
        """Garante que todos os diretórios necessários existam."""
        for directory in [cls.ASSETS_DIR, cls.IMAGE_GENERATED_DIR, 
                         cls.PROCESSED_DIR, cls.LOG_DIR, cls.PROMPT_DIR]:
            directory.mkdir(parents=True, exist_ok=True)