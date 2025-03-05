from fastapi import APIRouter, HTTPException, Query
import requests
from pymongo import MongoClient, errors
from pydantic import BaseModel
from typing import List, Dict, Optional
from logger import logger  
from fastapi.responses import JSONResponse
from analise import gerar_grafico_deputados_por_partido, gerar_grafico_deputados_por_estado

router = APIRouter()

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["camara_dados"]
deputados_collection = db["deputados"]
projetos_collection = db["projetos"]

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

# Modelo de dados (removido dataCadastro)
class Deputado(BaseModel):
    id: int
    nome: str
    siglaPartido: str
    uriPartido: str
    siglaUf: str
    idLegislatura: int
    urlFoto: str
    email: str

@router.get("/deputados", response_model=List[Deputado])
def listar_deputados(
    nome: Optional[str] = Query(None, description="Filtrar por nome ou parte do nome"),
    skip: int = Query(0, description="Número de registros a serem pulados"),
    limit: int = Query(10, description="Número máximo de registros a serem retornados (máx: 50)")
):
    try:
        filtros = {}

        # Filtro por nome (busca parcial, case-insensitive)
        if nome:
            filtros["nome"] = {"$regex": nome, "$options": "i"}

        # Limite máximo para evitar sobrecarga
        limit = min(limit, 50)

        # Consulta no banco de dados com paginação e filtros
        deputados = list(
            deputados_collection.find(filtros, {"_id": 0}).skip(skip).limit(limit)
        )

        logger.info(f"Consulta realizada com {len(deputados)} resultados")
        return deputados

    except errors.PyMongoError as e:
        logger.error(f"Erro no banco de dados: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.get("/deputados/{id}", response_model=Deputado)
def obter_deputado(id: int):
    try:
        deputado = deputados_collection.find_one({"id": id}, {"_id": 0})
        if not deputado:
            logger.warning(f"Deputado com ID {id} não encontrado")
            raise HTTPException(status_code=404, detail="Deputado não encontrado")
        
        logger.info(f"Deputado encontrado: {deputado['nome']}")
        return deputado
    except errors.PyMongoError as e:
        logger.error(f"Erro ao buscar deputado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.post("/deputados", response_model=Dict)
def criar_deputado(deputado: Deputado):
    try:
        if deputados_collection.find_one({"id": deputado.id}):
            logger.warning(f"Tentativa de cadastro duplicado para ID {deputado.id}")
            raise HTTPException(status_code=400, detail="Deputado já cadastrado")

        # Não estamos mais adicionando a dataCadastro
        deputados_collection.insert_one(deputado.dict())
        
        logger.info(f"Deputado {deputado.nome} cadastrado com sucesso")
        return {"message": "Deputado cadastrado com sucesso"}

    except errors.PyMongoError as e:
        logger.error(f"Erro ao cadastrar deputado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.put("/deputados/{id}", response_model=Dict)
def atualizar_deputado(id: int, deputado: Deputado):
    try:
        resultado = deputados_collection.update_one({"id": id}, {"$set": deputado.dict()})
        if resultado.matched_count == 0:
            logger.warning(f"Deputado com ID {id} não encontrado para atualização")
            raise HTTPException(status_code=404, detail="Deputado não encontrado")
        
        logger.info(f"Deputado {id} atualizado com sucesso")
        return {"message": "Deputado atualizado com sucesso"}

    except errors.PyMongoError as e:
        logger.error(f"Erro ao atualizar deputado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.delete("/deputados/{id}")
def deletar_deputado(id: int):
    try:
        resultado = deputados_collection.delete_one({"id": id})
        if resultado.deleted_count == 0:
            logger.warning(f"Deputado com ID {id} não encontrado para exclusão")
            raise HTTPException(status_code=404, detail="Deputado não encontrado")
        
        logger.info(f"Deputado {id} removido com sucesso")
        return {"message": "Deputado removido com sucesso"}

    except errors.PyMongoError as e:
        logger.error(f"Erro ao remover deputado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.get("/estatisticas/deputados-por-partido")
def deputados_por_partido():
    pipeline = [{"$group": {"_id": "$siglaPartido", "total": {"$sum": 1}}}, {"$sort": {"total": -1}}]
    resultado = list(deputados_collection.aggregate(pipeline))
    return {"deputados_por_partido": resultado}

@router.get("/estatisticas/deputados-por-estado")
def deputados_por_estado():
    pipeline = [{"$group": {"_id": "$siglaUf", "total": {"$sum": 1}}}, {"$sort": {"total": -1}}]
    resultado = list(deputados_collection.aggregate(pipeline))
    return {"deputados_por_estado": resultado}

@router.get("/estatisticas/grafico-deputados-por-partido")
def grafico_deputados_por_partido():
    imagem_base64 = gerar_grafico_deputados_por_partido()
    return JSONResponse(content={"imagem": f"data:image/png;base64,{imagem_base64}"})

@router.get("/estatisticas/grafico-deputados-por-estado")
def grafico_deputados_por_estado():
    imagem_base64 = gerar_grafico_deputados_por_estado()
    return JSONResponse(content={"imagem": f"data:image/png;base64,{imagem_base64}"})
