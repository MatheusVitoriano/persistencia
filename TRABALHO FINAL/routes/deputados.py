from fastapi import APIRouter, HTTPException, Query
import requests
from pymongo import MongoClient, errors
from pydantic import BaseModel
from typing import List, Dict, Optional
from logger import logger  
from datetime import datetime
from fastapi.responses import JSONResponse
from analise import gerar_grafico_deputados_por_partido, gerar_grafico_deputados_por_estado

router = APIRouter()

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["camara_dados"]
deputados_collection = db["deputados"]
projetos_collection = db["projetos"]

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

# Modelo de dados
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
def listar_deputados():
    
    try:
        deputados = list(deputados_collection.find({}, {"_id": 0}))
        return deputados
    except errors.PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

@router.get("/deputados/{id}", response_model=Deputado)
def obter_deputado(id: int):

    deputado = deputados_collection.find_one({"id": id}, {"_id": 0})
    if not deputado:
        raise HTTPException(status_code=404, detail="Deputado não encontrado")
    return deputado

@router.post("/deputados", response_model=Dict)
def criar_deputado(deputado: Deputado):
   
    if deputados_collection.find_one({"id": deputado.id}):
        raise HTTPException(status_code=400, detail="Deputado já cadastrado")

    deputados_collection.insert_one(deputado.dict())
    return {"message": "Deputado cadastrado com sucesso"}

@router.put("/deputados/{id}", response_model=Dict)
def atualizar_deputado(id: int, deputado: Deputado):
    
    resultado = deputados_collection.update_one({"id": id}, {"$set": deputado.dict()})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Deputado não encontrado")
    return {"message": "Deputado atualizado com sucesso"}

@router.delete("/deputados/{id}")
def deletar_deputado(id: int):
  
    resultado = deputados_collection.delete_one({"id": id})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Deputado não encontrado")
    return {"message": "Deputado removido com sucesso"}

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
    
    if not imagem_base64:
        raise HTTPException(status_code=404, detail="Dados insuficientes para gerar gráfico")

    return JSONResponse(content={"imagem": f"data:image/png;base64,{imagem_base64}"})

@router.get("/estatisticas/grafico-deputados-por-estado")
def grafico_deputados_por_estado():
 
    imagem_base64 = gerar_grafico_deputados_por_estado()
    
    if not imagem_base64:
        raise HTTPException(status_code=404, detail="Dados insuficientes para gerar gráfico")

    return JSONResponse(content={"imagem": f"data:image/png;base64,{imagem_base64}"})
