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
proposicoes_collection = db["proposicoes"]

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

# Modelo para validação das proposições
class Proposicao(BaseModel):
    id: int
    uri: str
    siglaTipo: str
    codTipo: int
    numero: int
    ano: int
    ementa: str

@router.get("/proposicoes", response_model=List[Proposicao])
def listar_proposicoes(
    siglaTipo: Optional[str] = Query(None, description="Filtrar por sigla do tipo de proposição (ex.: PL, PEC, MPV)"),
    ano: Optional[int] = Query(None, description="Filtrar pelo ano da proposição"),
    ementa: Optional[str] = Query(None, description="Filtrar por palavras-chave na ementa"),
    pagina: int = Query(1, ge=1, description="Número da página"),
    tamanho_pagina: int = Query(10, le=100, description="Quantidade de itens por página (máx: 100)")
):
   
    try:
        filtros = {}

        if siglaTipo:
            filtros["siglaTipo"] = {"$regex": siglaTipo, "$options": "i"}
        if ano:
            filtros["ano"] = ano
        if ementa:
            filtros["ementa"] = {"$regex": ementa, "$options": "i"}

        # Cálculo da paginação
        skip = (pagina - 1) * tamanho_pagina

        logger.info(f"Buscando proposições com filtros: {filtros} | Página: {pagina} | Tamanho: {tamanho_pagina}")

        proposicoes = list(proposicoes_collection.find(filtros, {"_id": 0}).skip(skip).limit(tamanho_pagina))

        if not proposicoes:
            logger.warning("Nenhuma proposição encontrada com os filtros aplicados.")
            raise HTTPException(status_code=404, detail="Nenhuma proposição encontrada")

        return proposicoes

    except errors.PyMongoError as e:
        logger.error(f"Erro no banco de dados ao buscar proposições: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.get("/proposicoes/{id}", response_model=Proposicao)
def detalhes_proposicao(id: int):
   
    try:
        logger.info(f"Buscando proposição com ID: {id}")
        proposicao = proposicoes_collection.find_one({"id": id}, {"_id": 0})

        if not proposicao:
            logger.info(f"Proposição ID {id} não encontrada no banco, buscando na API externa...")
            url = f"{BASE_URL}/proposicoes/{id}"
            response = requests.get(url)

            if response.status_code != 200:
                logger.warning(f"Proposição ID {id} não encontrada na API externa.")
                raise HTTPException(status_code=response.status_code, detail="Proposição não encontrada")

            proposicao = response.json().get("dados", {})
            if proposicao:
                proposicoes_collection.insert_one(proposicao)
                logger.info(f"Proposição ID {id} armazenada no banco local.")

        return proposicao

    except errors.PyMongoError as e:
        logger.error(f"Erro no banco de dados ao buscar proposição ID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.post("/proposicoes", response_model=Dict)
def criar_proposicao(proposicao: Proposicao):

    try:
        if proposicoes_collection.find_one({"id": proposicao.id}):
            logger.warning(f"Tentativa de adicionar proposição ID {proposicao.id} já existente.")
            raise HTTPException(status_code=400, detail="Proposição já cadastrada")

        resultado = proposicoes_collection.insert_one(proposicao.dict())

        if not resultado.inserted_id:
            logger.error(f"Falha ao inserir proposição ID {proposicao.id} no banco.")
            raise HTTPException(status_code=500, detail="Falha ao inserir proposição")

        logger.info(f"Proposição ID {proposicao.id} cadastrada com sucesso.")
        return {"message": "Proposição cadastrada com sucesso"}

    except errors.PyMongoError as e:
        logger.error(f"Erro ao adicionar proposição ID {proposicao.id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.put("/proposicoes/{id}", response_model=Dict)
def atualizar_proposicao(id: int, proposicao: Proposicao):
  
    try:
        resultado = proposicoes_collection.update_one({"id": id}, {"$set": proposicao.dict()})

        if resultado.matched_count == 0:
            logger.warning(f"Tentativa de atualizar proposição ID {id}, mas ela não foi encontrada.")
            raise HTTPException(status_code=404, detail="Proposição não encontrada")

        logger.info(f"Proposição ID {id} atualizada com sucesso.")
        return {"message": "Proposição atualizada com sucesso"}

    except errors.PyMongoError as e:
        logger.error(f"Erro ao atualizar proposição ID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.delete("/proposicoes/{id}")
def deletar_proposicao(id: int):
   
    try:
        resultado = proposicoes_collection.delete_one({"id": id})

        if resultado.deleted_count == 0:
            logger.warning(f"Tentativa de deletar proposição ID {id}, mas ela não foi encontrada.")
            raise HTTPException(status_code=404, detail="Proposição não encontrada")

        logger.info(f"Proposição ID {id} removida com sucesso.")
        return {"message": "Proposição removida com sucesso"}

    except errors.PyMongoError as e:
        logger.error(f"Erro ao deletar proposição ID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
