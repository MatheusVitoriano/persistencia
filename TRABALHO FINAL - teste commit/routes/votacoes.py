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
votacoes_collection = db["votacoes"]

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

# Modelo para validação das votações
class Votacao(BaseModel):
    id: str
    uri: str
    data: str
    dataHoraRegistro: str
    siglaOrgao: str
    uriOrgao: str
    uriEvento: Optional[str] = None    
    proposicaoObjeto: Optional[str] = None
    uriProposicaoObjeto: Optional[str] = None
    descricao: str
    aprovacao: int

@router.get("/votacoes", response_model=List[Votacao])
def listar_votacoes(
    siglaOrgao: Optional[str] = Query(None, description="Filtrar por sigla do órgão"),
    data: Optional[str] = Query(None, description="Filtrar por data da votação (YYYY-MM-DD)"),
    descricao: Optional[str] = Query(None, description="Filtrar por palavras-chave na descrição"),
    pagina: int = Query(1, ge=1, description="Número da página"),
    tamanho_pagina: int = Query(10, le=100, description="Quantidade de itens por página (máx: 100)")
):
   
    try:
        filtros = {}

        if siglaOrgao:
            filtros["siglaOrgao"] = {"$regex": siglaOrgao, "$options": "i"}
        if data:
            filtros["data"] = data
        if descricao:
            filtros["descricao"] = {"$regex": descricao, "$options": "i"}

        # Paginação
        skip = (pagina - 1) * tamanho_pagina

        logger.info(f"Buscando votações com filtros: {filtros} | Página: {pagina} | Tamanho: {tamanho_pagina}")

        votacoes = list(votacoes_collection.find(filtros, {"_id": 0}).skip(skip).limit(tamanho_pagina))

        if not votacoes:
            logger.warning("Nenhuma votação encontrada com os filtros aplicados.")
            raise HTTPException(status_code=404, detail="Nenhuma votação encontrada")

        return votacoes

    except errors.PyMongoError as e:
        logger.error(f"Erro no banco de dados ao buscar votações: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.get("/votacoes/{id}", response_model=Votacao)
def detalhes_votacao(id: str):
  
    try:
        logger.info(f"Buscando votação com ID: {id}")
        votacao = votacoes_collection.find_one({"id": id}, {"_id": 0})

        if not votacao:
            logger.info(f"Votação ID {id} não encontrada no banco, buscando na API externa...")
            url = f"{BASE_URL}/votacoes/{id}"
            response = requests.get(url)

            if response.status_code != 200:
                logger.warning(f"Votação ID {id} não encontrada na API externa.")
                raise HTTPException(status_code=response.status_code, detail="Votação não encontrada")

            votacao = response.json().get("dados", {})
            if votacao:
                votacoes_collection.insert_one(votacao)
                logger.info(f"Votação ID {id} armazenada no banco local.")

        return votacao

    except errors.PyMongoError as e:
        logger.error(f"Erro no banco de dados ao buscar votação ID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.post("/votacoes", response_model=Dict)
def criar_votacao(votacao: Votacao):
  
    try:
        if votacoes_collection.find_one({"id": votacao.id}):
            logger.warning(f"Tentativa de adicionar votação ID {votacao.id} já existente.")
            raise HTTPException(status_code=400, detail="Votação já cadastrada")

        votacoes_collection.insert_one(votacao.dict())
        logger.info(f"Votação ID {votacao.id} cadastrada com sucesso.")
        return {"message": "Votação cadastrada com sucesso"}

    except errors.PyMongoError as e:
        logger.error(f"Erro ao adicionar votação ID {votacao.id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.put("/votacoes/{id}", response_model=Dict)
def atualizar_votacao(id: str, votacao: Votacao):
  
    try:
        if not votacoes_collection.find_one({"id": id}):
            logger.warning(f"Tentativa de atualizar votação ID {id}, mas ela não foi encontrada.")
            raise HTTPException(status_code=404, detail="Votação não encontrada")

        votacoes_collection.update_one({"id": id}, {"$set": votacao.dict()})
        logger.info(f"Votação ID {id} atualizada com sucesso.")
        return {"message": "Votação atualizada com sucesso"}

    except errors.PyMongoError as e:
        logger.error(f"Erro ao atualizar votação ID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.delete("/votacoes/{id}")
def deletar_votacao(id: str):
   
    try:
        if not votacoes_collection.find_one({"id": id}):
            logger.warning(f"Tentativa de deletar votação ID {id}, mas ela não foi encontrada.")
            raise HTTPException(status_code=404, detail="Votação não encontrada")

        votacoes_collection.delete_one({"id": id})
        logger.info(f"Votação ID {id} removida com sucesso.")
        return {"message": "Votação removida com sucesso"}

    except errors.PyMongoError as e:
        logger.error(f"Erro ao deletar votação ID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
