import logging

# Configuração básica do logging
logging.basicConfig(
    level=logging.INFO,  # Define o nível mínimo de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Salva os logs no arquivo "app.log"
        logging.StreamHandler()  # Exibe os logs no console
    ]
)

# Criar um logger específico para a aplicação
logger = logging.getLogger("FastAPI-Logger")
