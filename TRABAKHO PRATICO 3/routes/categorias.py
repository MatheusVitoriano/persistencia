from fastapi import APIRouter, HTTPException, Query
from config import categorias_collection
from models import Categoria
from typing import List

router = APIRouter()

### F1: INSERIR UMA CATEGORIA ###
@router.post("/", response_model=Categoria)
def criar_categoria(categoria: Categoria):
    categoria_dict = categoria.dict(by_alias=True)
    result = categorias_collection.insert_one(categoria_dict)
    categoria_dict["_id"] = str(result.inserted_id)
    return categoria_dict

### F2: LISTAR TODAS AS CATEGORIAS ###
@router.get("/", response_model=List[Categoria])
def listar_categorias():
    categorias = list(categorias_collection.find())
    for categoria in categorias:
        categoria["_id"] = str(categoria["_id"])  # Converter ObjectId para string
    return categorias

### F3: CRUD COMPLETO ###
@router.get("/{categoria_id}", response_model=Categoria)
def obter_categoria(categoria_id: str):
    categoria = categorias_collection.find_one({"_id": categoria_id})
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    categoria["_id"] = str(categoria["_id"])
    return categoria

@router.put("/{categoria_id}", response_model=Categoria)
def atualizar_categoria(categoria_id: str, categoria: Categoria):
    categoria_dict = categoria.dict(by_alias=True)
    result = categorias_collection.update_one({"_id": categoria_id}, {"$set": categoria_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria_dict

@router.delete("/{categoria_id}")
def deletar_categoria(categoria_id: str):
    result = categorias_collection.delete_one({"_id": categoria_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return {"message": "Categoria deletada com sucesso"}

### F4: MOSTRAR QUANTIDADE DE CATEGORIAS ###
@router.get("/quantidade/")
def contar_categorias():
    count = categorias_collection.count_documents({})
    return {"quantidade": count}

### F5: PAGINAÇÃO DE CATEGORIAS ###
@router.get("/paginado/", response_model=List[Categoria])
def listar_categorias_paginadas(page: int = Query(1, alias="page"), limit: int = Query(10, alias="limit")):
    offset = (page - 1) * limit
    categorias = list(categorias_collection.find().skip(offset).limit(limit))
    for categoria in categorias:
        categoria["_id"] = str(categoria["_id"])
    return categorias

### F6: FILTRAR CATEGORIAS POR ATRIBUTOS ###
@router.get("/filtrar/", response_model=List[Categoria])
def filtrar_categorias(nome: str = None):
    filtro = {}
    if nome:
        filtro["nome"] = {"$regex": nome, "$options": "i"}  # Case insensitive

    categorias = list(categorias_collection.find(filtro))
    for categoria in categorias:
        categoria["_id"] = str(categoria["_id"])
    return categorias
