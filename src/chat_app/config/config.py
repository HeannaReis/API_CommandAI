# src/config/config.py
import os
from pathlib import Path

class Config:
    # Aponte para a raiz do projeto API_CommandAI (3 níveis acima de src/config/config.py)
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    print(f"Base Directory: {BASE_DIR}") # ESTE LOG DEVE MUDAR PARA A RAIZ DO PROJETO!

    # Ajuste os caminhos relativos à NOVA BASE_DIR
    # Exemplo: Se 'assets' está em 'API_CommandAI/src/assets'
    ASSETS_DIR = BASE_DIR / "src" / "assets"
    print(f"Assets Directory: {ASSETS_DIR}") # Verifique este log também

    # Caminhos para prompts dinâmicos
    # Exemplo: Se 'prompt' está em 'API_CommandAI/src/chat_app/prompt'
    PROMPT_DIR = BASE_DIR / "src" / "chat_app" / "prompt"
    PROMPT_CHAT_FILE = PROMPT_DIR / "prompt_chat.txt"

    # Configuração de logs
    # Exemplo: Se 'logs' está diretamente na raiz 'API_CommandAI/logs'
    LOG_DIR = BASE_DIR / "logs"
    # Ou se está em 'API_CommandAI/src/chat_app/logs':
    # LOG_DIR = BASE_DIR / "src" / "chat_app" / "logs"

    # Configuração de histórico
    # Exemplo: Se 'historico_analises.json' está em 'API_CommandAI/src/chat_app/historico_analises.json'
    HISTORY_FILE = BASE_DIR / "src" / "chat_app" / "historico_analises.json"

    # Configuração de rate limiting (mantém-se)
    CHAT_RATE_LIMIT = {"max_requests": 9, "period_seconds": 60}
    API_RATE_LIMIT = {"max_requests": 9, "period_seconds": 60}

    @classmethod
    def ensure_directories(cls):
        """Garante que todos os diretórios necessários existam."""
        for directory in [cls.ASSETS_DIR,
                          cls.LOG_DIR, cls.PROMPT_DIR]:
            directory.mkdir(parents=True, exist_ok=True)