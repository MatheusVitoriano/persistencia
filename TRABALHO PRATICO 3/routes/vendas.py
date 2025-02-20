from fastapi import APIRouter, HTTPException, Query, Depends
from config import vendas_collection
from models import Venda
from typing import List
from pymongo import MongoClient
from config import get_database

router = APIRouter()

### F1: INSERIR UMA VENDA ###
@router.post("/", response_model=Venda)
def criar_venda(venda: Venda):
    venda_dict = venda.dict(by_alias=True)
    result = vendas_collection.insert_one(venda_dict)
    venda_dict["_id"] = str(result.inserted_id)
    return venda_dict

### F2: LISTAR TODAS AS VENDAS ###
@router.get("/", response_model=List[Venda])
def listar_vendas():
    vendas = list(vendas_collection.find())
    for venda in vendas:
        venda["_id"] = str(venda["_id"])  # Converter ObjectId para string
    return vendas

### F3: CRUD COMPLETO ###
@router.get("/{venda_id}", response_model=Venda)
def obter_venda(venda_id: str):
    venda = vendas_collection.find_one({"_id": venda_id})
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    venda["_id"] = str(venda["_id"])
    return venda

@router.put("/{venda_id}", response_model=Venda)
def atualizar_venda(venda_id: str, venda: Venda):
    venda_dict = venda.dict(by_alias=True)
    result = vendas_collection.update_one({"_id": venda_id}, {"$set": venda_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda_dict

@router.delete("/{venda_id}")
def deletar_venda(venda_id: str):
    result = vendas_collection.delete_one({"_id": venda_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return {"message": "Venda deletada com sucesso"}

### F4: MOSTRAR QUANTIDADE DE VENDAS ###
@router.get("/quantidade/")
def contar_vendas():
    count = vendas_collection.count_documents({})
    return {"quantidade": count}

### F5: PAGINAÇÃO DE VENDAS ###
@router.get("/paginado/", response_model=List[Venda])
def listar_vendas_paginadas(page: int = Query(1, alias="page"), limit: int = Query(10, alias="limit")):
    offset = (page - 1) * limit
    vendas = list(vendas_collection.find().skip(offset).limit(limit))
    for venda in vendas:
        venda["_id"] = str(venda["_id"])
    return vendas

### F6: FILTRAR VENDAS POR ATRIBUTOS ###
@router.get("/filtrar/", response_model=List[Venda])
def filtrar_vendas(data: str = None, forma_pagamento: str = None):
    filtro = {}
    if data:
        filtro["data"] = data  # Buscar vendas por data exata
    if forma_pagamento:
        filtro["forma_pagamento"] = {"$regex": forma_pagamento, "$options": "i"}  # Case insensitive

    vendas = list(vendas_collection.find(filtro))
    for venda in vendas:
        venda["_id"] = str(venda["_id"])
    return vendas

#Consulta complexa
@router.get("/vendas/detalhes")
async def listar_vendas_detalhadas(db=Depends(get_database)):
    pipeline = [
        {
            "$lookup": {
                "from": "clientes",
                "localField": "cliente_id",
                "foreignField": "_id",
                "as": "cliente"
            }
        },
        {
            "$lookup": {
                "from": "jogos",
                "localField": "jogos_id",
                "foreignField": "_id",
                "as": "jogos"
            }
        },
        {
            "$project": {
                "data": 1,
                "valor_total": 1,
                "forma_pagamento": 1,
                "desconto": 1,
                "cliente.nome": 1,
                "cliente.email": 1,
                "jogos.nome": 1
            }
        }
    ]
    
    vendas = list(db["vendas"].aggregate(pipeline))
    return vendas
