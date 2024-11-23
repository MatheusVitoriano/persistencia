from fastapi import FastAPI, HTTPException
import yaml
import json
import logging

#Utilizei o FastAPI pq é mais simples.

app = FastAPI()

# Configuração inicial
def configure_logging(config):
    logging.basicConfig(
        level=getattr(logging, config["logging"]["level"]),
        format=config["logging"]["format"],
        filename=config["logging"]["file"]
    )

def load_config():
    with open("config.yaml", "r") as config_file:
        return yaml.safe_load(config_file)

# Carregar configurações
config = load_config()
configure_logging(config)

# Função para processar os dados
def process_data(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            logging.info(f"Arquivo JSON '{file_path}' carregado com sucesso.")
            valid_data = []
            invalid_data = []

            for record in data:
                if record.get("age") is not None:
                    logging.info(f"Processando registro válido: {record}")
                    valid_data.append(record)
                else:
                    logging.warning(f"Registro inválido encontrado: {record}")
                    invalid_data.append(record)

            return {"valid_data": valid_data, "invalid_data": invalid_data}

    except Exception as e:
        logging.error(f"Erro ao processar o arquivo JSON: {e}")
        raise

# Rotas
@app.get("/")
def read_root():
    return {"message": "Funcionando"}

@app.get("/process")
def process_endpoint():
    try:
        file_path = config["data"]["file"]
        result = process_data(file_path)
        return {"status": "success", "data": result}
    except Exception as e:
        logging.critical(f"Erro crítico no endpoint '/process': {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar os dados.")
