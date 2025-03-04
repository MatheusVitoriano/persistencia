from fastapi import APIRouter, HTTPException, Query
import requests
from pymongo import MongoClient, errors
from pydantic import BaseModel
from typing import List, Optional, Dict
from logger import logger

router = APIRouter()

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["camara_dados"]
orgaos_collection = db["orgaos"]

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

# Modelo para validação dos órgãos
class Orgao(BaseModel):
    id: int
    uri: str
    sigla: str
    nome: str
    apelido: Optional[str]
    codTipoOrgao: int
    tipoOrgao: str
    nomePublicacao: str
    nomeResumido: Optional[str]

@router.get("/orgaos", response_model=List[Orgao])
def listar_orgaos(
    sigla: Optional[str] = Query(None, description="Filtrar por sigla"),
    nome: Optional[str] = Query(None, description="Filtrar por nome"),
    tipoOrgao: Optional[str] = Query(None, description="Filtrar pelo tipo de órgão"),
    pagina: int = Query(1, ge=1, description="Número da página"),
    tamanho_pagina: int = Query(10, le=100, description="Quantidade de itens por página (máx: 100)")
):
    
    try:
        filtros = {}

        if sigla:
            filtros["sigla"] = {"$regex": sigla, "$options": "i"}
        if nome:
            filtros["nome"] = {"$regex": nome, "$options": "i"}
        if tipoOrgao:
            filtros["tipoOrgao"] = {"$regex": tipoOrgao, "$options": "i"}

        # Cálculo da paginação
        skip = (pagina - 1) * tamanho_pagina

        logger.info(f"Buscando órgãos com filtros: {filtros} | Página: {pagina} | Tamanho: {tamanho_pagina}")

        orgaos = list(orgaos_collection.find(filtros, {"_id": 0}).skip(skip).limit(tamanho_pagina))

        if not orgaos:
            logger.warning("Nenhum órgão encontrado com os filtros aplicados.")
            raise HTTPException(status_code=404, detail="Nenhum órgão encontrado")

        return orgaos

    except errors.PyMongoError as e:
        logger.error(f"Erro no banco de dados ao buscar órgãos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.get("/orgaos/{id}", response_model=Orgao)
def obter_orgao(id: int):
  
    try:
        logger.info(f"Buscando órgão com ID: {id}")
        orgao = orgaos_collection.find_one({"id": id}, {"_id": 0})

        if not orgao:
            logger.info(f"Órgão ID {id} não encontrado no banco, buscando na API externa...")
            url = f"{BASE_URL}/orgaos/{id}"
            response = requests.get(url)

            if response.status_code != 200:
                logger.warning(f"Órgão ID {id} não encontrado na API externa.")
                raise HTTPException(status_code=response.status_code, detail="Órgão não encontrado")

            orgao = response.json().get("dados", {})
            if orgao:
                orgaos_collection.insert_one(orgao)
                logger.info(f"Órgão ID {id} armazenado no banco local.")

        return orgao

    except errors.PyMongoError as e:
        logger.error(f"Erro no banco de dados ao buscar órgão ID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.post("/orgaos", response_model=Dict)
def adicionar_orgao(orgao: Orgao):
    
    try:
        if orgaos_collection.find_one({"id": orgao.id}):
            logger.warning(f"Tentativa de adicionar órgão ID {orgao.id} já existente.")
            raise HTTPException(status_code=400, detail="Órgão já cadastrado")

        resultado = orgaos_collection.insert_one(orgao.dict())

        if not resultado.inserted_id:
            logger.error(f"Falha ao inserir órgão ID {orgao.id} no banco.")
            raise HTTPException(status_code=500, detail="Falha ao inserir órgão")

        logger.info(f"Órgão ID {orgao.id} adicionado com sucesso.")
        return {"mensagem": "Órgão adicionado com sucesso"}

    except errors.PyMongoError as e:
        logger.error(f"Erro ao adicionar órgão ID {orgao.id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.put("/orgaos/{id}", response_model=Dict)
def atualizar_orgao(id: int, novos_dados: Orgao):
  
    try:
        resultado = orgaos_collection.update_one({"id": id}, {"$set": novos_dados.dict()})

        if resultado.matched_count == 0:
            logger.warning(f"Tentativa de atualizar órgão ID {id}, mas ele não foi encontrado.")
            raise HTTPException(status_code=404, detail="Órgão não encontrado")

        logger.info(f"Órgão ID {id} atualizado com sucesso.")
        return {"mensagem": "Órgão atualizado com sucesso"}

    except errors.PyMongoError as e:
        logger.error(f"Erro ao atualizar órgão ID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.delete("/orgaos/{id}", response_model=Dict)
def deletar_orgao(id: int):
   
    try:
        resultado = orgaos_collection.delete_one({"id": id})

        if resultado.deleted_count == 0:
            logger.warning(f"Tentativa de deletar órgão ID {id}, mas ele não foi encontrado.")
            raise HTTPException(status_code=404, detail="Órgão não encontrado")

        logger.info(f"Órgão ID {id} removido com sucesso.")
        return {"mensagem": "Órgão removido com sucesso"}

    except errors.PyMongoError as e:
        logger.error(f"Erro ao deletar órgão ID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
