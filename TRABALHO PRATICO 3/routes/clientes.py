from fastapi import APIRouter, HTTPException, Query
from config import clientes_collection
from models import Cliente
from typing import List

router = APIRouter()

### F1: INSERIR UM CLIENTE ###
@router.post("/", response_model=Cliente)
def criar_cliente(cliente: Cliente):
    cliente_dict = cliente.dict(by_alias=True)
    result = clientes_collection.insert_one(cliente_dict)
    cliente_dict["_id"] = str(result.inserted_id)
    return cliente_dict

### F2: LISTAR TODOS OS CLIENTES ###
@router.get("/", response_model=List[Cliente])
def listar_clientes():
    clientes = list(clientes_collection.find())
    for cliente in clientes:
        cliente["_id"] = str(cliente["_id"])  # Converter ObjectId para string
    return clientes

### F3: CRUD COMPLETO ###
@router.get("/{cliente_id}", response_model=Cliente)
def obter_cliente(cliente_id: str):
    cliente = clientes_collection.find_one({"_id": cliente_id})
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    cliente["_id"] = str(cliente["_id"])
    return cliente

@router.put("/{cliente_id}", response_model=Cliente)
def atualizar_cliente(cliente_id: str, cliente: Cliente):
    cliente_dict = cliente.dict(by_alias=True)
    result = clientes_collection.update_one({"_id": cliente_id}, {"$set": cliente_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente_dict

@router.delete("/{cliente_id}")
def deletar_cliente(cliente_id: str):
    result = clientes_collection.delete_one({"_id": cliente_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"message": "Cliente deletado com sucesso"}

### F4: MOSTRAR QUANTIDADE DE CLIENTES ###
@router.get("/quantidade/")
def contar_clientes():
    count = clientes_collection.count_documents({})
    return {"quantidade": count}

### F5: PAGINAÇÃO DE CLIENTES ###
@router.get("/paginado/", response_model=List[Cliente])
def listar_clientes_paginados(page: int = Query(1, alias="page"), limit: int = Query(10, alias="limit")):
    offset = (page - 1) * limit
    clientes = list(clientes_collection.find().skip(offset).limit(limit))
    for cliente in clientes:
        cliente["_id"] = str(cliente["_id"])
    return clientes

### F6: FILTRAR CLIENTES POR ATRIBUTOS ###
@router.get("/filtrar/", response_model=List[Cliente])
def filtrar_clientes(nome: str = None, email: str = None):
    filtro = {}
    if nome:
        filtro["nome"] = {"$regex": nome, "$options": "i"}  # Busca por nome, case insensitive
    if email:
        filtro["email"] = email  # Busca exata por email

    clientes = list(clientes_collection.find(filtro))
    for cliente in clientes:
        cliente["_id"] = str(cliente["_id"])
    return clientes
