# core/logger_config.py
import logging
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

log_filename = datetime.now().strftime("log_%Y%m%d.log")
log_filepath = os.path.join(LOG_DIR, log_filename)

logging.basicConfig(
    # ALTERE ESTA LINHA PARA logging.DEBUG PARA VER TODOS OS DETALHES!
    level=logging.DEBUG, # <--- Mude de logging.INFO para logging.DEBUG
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filepath, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)