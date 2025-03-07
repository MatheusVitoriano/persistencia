from fastapi import APIRouter, HTTPException
import requests
from pymongo import MongoClient, errors
from pydantic import BaseModel
from typing import List, Dict
from logger import logger

router = APIRouter()

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["camara_dados"]
partidos_collection = db["partidos"]

# Criar índice único para o campo 'id' na coleção 'partidos' (somente uma vez ao iniciar o servidor)
partidos_collection.create_index([("id", 1)], unique=True)

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

# Modelo para validação dos partidos
class Partido(BaseModel):
    id: int
    nome: str
    sigla: str
    uri: str

@router.get("/partidos", response_model=List[Partido])
def listar_partidos(pagina: int = 1, tamanho_pagina: int = 10, sigla: str = None):
   
    try:
        # Construir o filtro de consulta
        filtro = {}
        if sigla:
            filtro["sigla"] = sigla.upper()  # Normalizar a sigla para maiúsculas

        # Paginação de partidos com filtro opcional
        partidos = list(partidos_collection.find(filtro, {"_id": 0}).skip((pagina - 1) * tamanho_pagina).limit(tamanho_pagina))

        if not partidos:
            logger.warning("Nenhum partido encontrado no banco de dados. Carregando da API...")

            # Carregar os partidos da API se não houver nenhum no banco
            url = f"{BASE_URL}/partidos?pagina={pagina}&itens={tamanho_pagina}"
            response = requests.get(url)

            if response.status_code != 200:
                logger.warning(f"Erro ao buscar partidos na API externa: {response.status_code}")
                raise HTTPException(status_code=response.status_code, detail="Erro ao buscar partidos na API externa")

            dados_partidos = response.json().get("dados", [])
            if dados_partidos:
                partidos_collection.insert_many(dados_partidos)
                logger.info(f"{len(dados_partidos)} partidos foram armazenados no banco de dados.")

            partidos = dados_partidos  # Atribui os partidos obtidos da API

        logger.info(f"Partidos encontrados: {len(partidos)}")
        return partidos

    except errors.PyMongoError as e:
        logger.error(f"Erro no banco de dados ao buscar partidos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")


@router.get("/partidos/{id}", response_model=Partido)
def detalhes_partido(id: int):
 
    try:
        partido = partidos_collection.find_one({"id": id}, {"_id": 0})

        if not partido:
            logger.info(f"Partido ID {id} não encontrado no banco, buscando na API externa...")
            url = f"{BASE_URL}/partidos/{id}"
            response = requests.get(url)

            if response.status_code != 200:
                logger.warning(f"Partido ID {id} não encontrado na API externa.")
                raise HTTPException(status_code=response.status_code, detail="Partido não encontrado")

            partido = response.json().get("dados", {})
            if partido:
                partidos_collection.insert_one(partido)
                logger.info(f"Partido ID {id} armazenado no banco local.")

        return partido

    except errors.PyMongoError as e:
        logger.error(f"Erro no banco de dados ao buscar partido ID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.post("/partidos", response_model=Dict)
def criar_partido(partido: Partido):
  
    try:
        # Verificar se o partido já existe no banco de dados pelo 'id'
        if partidos_collection.find_one({"id": partido.id}):
            logger.warning(f"Tentativa de adicionar partido ID {partido.id} já existente.")
            raise HTTPException(status_code=400, detail="Partido já cadastrado")

        # Inserir o novo partido
        partidos_collection.insert_one(partido.dict())
        logger.info(f"Partido ID {partido.id} cadastrado com sucesso.")
        return {"message": "Partido cadastrado com sucesso"}

    except errors.DuplicateKeyError:
        # Caso o índice único de 'id' seja violado
        logger.warning(f"Partido com ID {partido.id} já existe no banco de dados.")
        raise HTTPException(status_code=400, detail="Partido já cadastrado no banco")

    except errors.PyMongoError as e:
        logger.error(f"Erro ao adicionar partido ID {partido.id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.put("/partidos/{id}", response_model=Dict)
def atualizar_partido(id: int, partido: Partido):
  
    try:
        if not partidos_collection.find_one({"id": id}):
            logger.warning(f"Tentativa de atualizar partido ID {id}, mas ele não foi encontrado.")
            raise HTTPException(status_code=404, detail="Partido não encontrado")

        partidos_collection.update_one({"id": id}, {"$set": partido.dict()})
        logger.info(f"Partido ID {id} atualizado com sucesso.")
        return {"message": "Partido atualizado com sucesso"}

    except errors.PyMongoError as e:
        logger.error(f"Erro ao atualizar partido ID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.delete("/partidos/{id}")
def deletar_partido(id: int):
   
    try:
        if not partidos_collection.find_one({"id": id}):
            logger.warning(f"Tentativa de deletar partido ID {id}, mas ele não foi encontrado.")
            raise HTTPException(status_code=404, detail="Partido não encontrado")

        partidos_collection.delete_one({"id": id})
        logger.info(f"Partido ID {id} removido com sucesso.")
        return {"message": "Partido removido com sucesso"}

    except errors.PyMongoError as e:
        logger.error(f"Erro ao deletar partido ID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
