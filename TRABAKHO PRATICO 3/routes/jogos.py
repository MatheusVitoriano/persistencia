from fastapi import APIRouter, HTTPException, Query, Depends
from config import jogos_collection, get_database
from models import Jogo
from typing import List

router = APIRouter()

### F1: INSERIR UM JOGO ###
@router.post("/", response_model=Jogo)
def criar_jogo(jogo: Jogo):
    jogo_dict = jogo.dict(by_alias=True)
    result = jogos_collection.insert_one(jogo_dict)
    jogo_dict["_id"] = str(result.inserted_id)
    return jogo_dict

### F2: LISTAR TODOS OS JOGOS ###
@router.get("/", response_model=List[Jogo])
def listar_jogos():
    jogos = list(jogos_collection.find())
    for jogo in jogos:
        jogo["_id"] = str(jogo["_id"])  # Converter ObjectId para string
    return jogos

### F3: CRUD COMPLETO ###
@router.get("/{jogo_id}", response_model=Jogo)
def obter_jogo(jogo_id: str):
    jogo = jogos_collection.find_one({"_id": jogo_id})
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    jogo["_id"] = str(jogo["_id"])
    return jogo

@router.put("/{jogo_id}", response_model=Jogo)
def atualizar_jogo(jogo_id: str, jogo: Jogo):
    jogo_dict = jogo.dict(by_alias=True)
    result = jogos_collection.update_one({"_id": jogo_id}, {"$set": jogo_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return jogo_dict

@router.delete("/{jogo_id}")
def deletar_jogo(jogo_id: str):
    result = jogos_collection.delete_one({"_id": jogo_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return {"message": "Jogo deletado com sucesso"}

### F4: MOSTRAR QUANTIDADE DE JOGOS ###
@router.get("/quantidade/")
def contar_jogos():
    count = jogos_collection.count_documents({})
    return {"quantidade": count}

### F5: PAGINAÇÃO DE JOGOS ###
@router.get("/paginado/", response_model=List[Jogo])
def listar_jogos_paginados(page: int = Query(1, alias="page"), limit: int = Query(10, alias="limit")):
    offset = (page - 1) * limit
    jogos = list(jogos_collection.find().skip(offset).limit(limit))
    for jogo in jogos:
        jogo["_id"] = str(jogo["_id"])
    return jogos

### F6: FILTRAR JOGOS POR ATRIBUTOS ###
@router.get("/filtrar/", response_model=List[Jogo])
def filtrar_jogos(nome: str = None, desenvolvedor: str = None, preco_min: float = None, preco_max: float = None):
    filtro = {}
    if nome:
        filtro["nome"] = {"$regex": nome, "$options": "i"}  # Case insensitive
    if desenvolvedor:
        filtro["desenvolvedor"] = {"$regex": desenvolvedor, "$options": "i"}
    if preco_min is not None and preco_max is not None:
        filtro["preco"] = {"$gte": preco_min, "$lte": preco_max}
    elif preco_min is not None:
        filtro["preco"] = {"$gte": preco_min}
    elif preco_max is not None:
        filtro["preco"] = {"$lte": preco_max}

    jogos = list(jogos_collection.find(filtro))
    for jogo in jogos:
        jogo["_id"] = str(jogo["_id"])
    return jogos

@router.get("/jogos/detalhes")
async def listar_jogos_detalhados(db=Depends(get_database)):
    pipeline = [
        {
            "$lookup": {
                "from": "categorias",
                "localField": "categoria_id",
                "foreignField": "_id",
                "as": "categoria"
            }
        },
        {
            "$lookup": {
                "from": "plataformas",
                "localField": "plataforma_id",
                "foreignField": "_id",
                "as": "plataforma"
            }
        },
        {
            "$project": {
                "nome": 1,
                "desenvolvedor": 1,
                "preco": 1,
                "estoque": 1,
                "data_lancamento": 1,
                "categoria.nome": 1,
                "plataforma.nome": 1
            }
        }
    ]
    
    jogos = list(db["jogos"].aggregate(pipeline))
    return jogos
