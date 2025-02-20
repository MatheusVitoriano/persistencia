from fastapi import APIRouter, HTTPException, Query
from config import plataformas_collection
from models import Plataforma
from typing import List

router = APIRouter()

### F1: INSERIR UMA PLATAFORMA ###
@router.post("/", response_model=Plataforma)
def criar_plataforma(plataforma: Plataforma):
    plataforma_dict = plataforma.dict(by_alias=True)
    result = plataformas_collection.insert_one(plataforma_dict)
    plataforma_dict["_id"] = str(result.inserted_id)
    return plataforma_dict

### F2: LISTAR TODAS AS PLATAFORMAS ###
@router.get("/", response_model=List[Plataforma])
def listar_plataformas():
    plataformas = list(plataformas_collection.find())
    for plataforma in plataformas:
        plataforma["_id"] = str(plataforma["_id"])  # Converter ObjectId para string
    return plataformas

### F3: CRUD COMPLETO ###
@router.get("/{plataforma_id}", response_model=Plataforma)
def obter_plataforma(plataforma_id: str):
    plataforma = plataformas_collection.find_one({"_id": plataforma_id})
    if not plataforma:
        raise HTTPException(status_code=404, detail="Plataforma não encontrada")
    plataforma["_id"] = str(plataforma["_id"])
    return plataforma

@router.put("/{plataforma_id}", response_model=Plataforma)
def atualizar_plataforma(plataforma_id: str, plataforma: Plataforma):
    plataforma_dict = plataforma.dict(by_alias=True)
    result = plataformas_collection.update_one({"_id": plataforma_id}, {"$set": plataforma_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Plataforma não encontrada")
    return plataforma_dict

@router.delete("/{plataforma_id}")
def deletar_plataforma(plataforma_id: str):
    result = plataformas_collection.delete_one({"_id": plataforma_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Plataforma não encontrada")
    return {"message": "Plataforma deletada com sucesso"}

### F4: MOSTRAR QUANTIDADE DE PLATAFORMAS ###
@router.get("/quantidade/")
def contar_plataformas():
    count = plataformas_collection.count_documents({})
    return {"quantidade": count}

### F5: PAGINAÇÃO DE PLATAFORMAS ###
@router.get("/paginado/", response_model=List[Plataforma])
def listar_plataformas_paginadas(page: int = Query(1, alias="page"), limit: int = Query(10, alias="limit")):
    offset = (page - 1) * limit
    plataformas = list(plataformas_collection.find().skip(offset).limit(limit))
    for plataforma in plataformas:
        plataforma["_id"] = str(plataforma["_id"])
    return plataformas

### F6: FILTRAR PLATAFORMAS POR ATRIBUTOS ###
@router.get("/filtrar/", response_model=List[Plataforma])
def filtrar_plataformas(nome: str = None, fabricante: str = None):
    filtro = {}
    if nome:
        filtro["nome"] = {"$regex": nome, "$options": "i"}  # Case insensitive
    if fabricante:
        filtro["fabricante"] = {"$regex": fabricante, "$options": "i"}

    plataformas = list(plataformas_collection.find(filtro))
    for plataforma in plataformas:
        plataforma["_id"] = str(plataforma["_id"])
    return plataformas
