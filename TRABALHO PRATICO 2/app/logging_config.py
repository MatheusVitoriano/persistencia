import logging
from logging.handlers import RotatingFileHandler

# Configurar o logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("app.log", maxBytes=5_000_000, backupCount=5),  # Log rotativo
        logging.StreamHandler(),  # Exibe logs no terminal
    ],
)

# Função para obter o logger
def get_logger(name: str):
    return logging.getLogger(name)
