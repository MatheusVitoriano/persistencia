from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Jogo
from pydantic import BaseModel
from datetime import date
from sqlalchemy import extract
from app.logging_config import get_logger  # Importar o logger



# Criar o roteador
router = APIRouter()

logger = get_logger("JogoRoutes")  # Instância de logger para esta rota

# Esquema de entrada para Jogo
class JogoCreate(BaseModel):
    nome: str
    desenvolvedor: str
    preco: float
    estoque: int
    data_lancamento: date


#Criar um novo jogo
@router.post("/jogos/", response_model=dict)
def criar_jogo(jogo: JogoCreate, db: Session = Depends(get_db)):
    """
    Insere um novo jogo no banco de dados.

    Args:
        jogo (JogoCreate): Dados do jogo enviados no corpo da requisição.
        db (Session): Sessão do banco de dados injetada automaticamente.

    Returns:
        dict: Confirmação do jogo criado.
    """
    novo_jogo = Jogo(
        nome=jogo.nome,
        desenvolvedor=jogo.desenvolvedor,
        preco=jogo.preco,
        estoque=jogo.estoque,
        data_lancamento=jogo.data_lancamento
    )
    try:
        db.add(novo_jogo)
        db.commit()
        db.refresh(novo_jogo)
        return {"message": "Jogo criado com sucesso", "id": novo_jogo.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar jogo: {e}")


#listar todos os jogos
@router.get("/jogos/", response_model=list[dict])
def listar_jogos(db: Session = Depends(get_db)):
    """
    Lista todos os jogos cadastrados no banco de dados.

    Args:
        db (Session): Sessão do banco de dados injetada automaticamente.

    Returns:
        list[dict]: Lista de jogos cadastrados no formato JSON.
    """
    try:
        jogos = db.query(Jogo).all()
        return [
            {
                "id": jogo.id,
                "nome": jogo.nome,
                "desenvolvedor": jogo.desenvolvedor,
                "preco": jogo.preco,
                "estoque": jogo.estoque,
                "data_lancamento": jogo.data_lancamento,
            }
            for jogo in jogos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar jogos: {e}")
    
#Contagem de jogos
@router.get("/jogos/quantidade", response_model=dict)
def contar_jogos(db: Session = Depends(get_db)):
    """
    Conta a quantidade total de jogos cadastrados.

    Args:
        db (Session): Sessão do banco de dados injetada automaticamente.

    Returns:
        dict: Contagem total de jogos.
    """
    try:
        quantidade = db.query(Jogo).count()
        return {"quantidade": quantidade}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar jogos: {e}")
    
#Ler um registro especifico
@router.get("/jogos/{jogo_id}", response_model=dict)
def consultar_jogo(jogo_id: int, db: Session = Depends(get_db)):
    """
    Consultar um jogo específico pelo ID.

    Args:
        jogo_id (int): ID do jogo.
        db (Session): Sessão do banco de dados injetada automaticamente.

    Returns:
        dict: Dados do jogo.
    """
    jogo = db.query(Jogo).filter(Jogo.id == jogo_id).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return {
        "id": jogo.id,
        "nome": jogo.nome,
        "desenvolvedor": jogo.desenvolvedor,
        "preco": jogo.preco,
        "estoque": jogo.estoque,
        "data_lancamento": jogo.data_lancamento,
    }

# Atualizar um registro especifico
@router.put("/jogos/{jogo_id}", response_model=dict)
def atualizar_jogo(jogo_id: int, jogo: JogoCreate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um jogo específico.

    Args:
        jogo_id (int): ID do jogo a ser atualizado.
        jogo (JogoCreate): Dados atualizados do jogo.
        db (Session): Sessão do banco de dados injetada automaticamente.

    Returns:
        dict: Confirmação do jogo atualizado.
    """
    jogo_existente = db.query(Jogo).filter(Jogo.id == jogo_id).first()
    if not jogo_existente:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    try:
        jogo_existente.nome = jogo.nome
        jogo_existente.desenvolvedor = jogo.desenvolvedor
        jogo_existente.preco = jogo.preco
        jogo_existente.estoque = jogo.estoque
        jogo_existente.data_lancamento = jogo.data_lancamento

        db.commit()
        db.refresh(jogo_existente)
        return {"message": "Jogo atualizado com sucesso", "id": jogo_existente.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar jogo: {e}")
    

#Excluir um registro especifico
@router.delete("/jogos/{jogo_id}", response_model=dict)
def excluir_jogo(jogo_id: int, db: Session = Depends(get_db)):
    """
    Exclui um jogo específico pelo ID.

    Args:
        jogo_id (int): ID do jogo a ser excluído.
        db (Session): Sessão do banco de dados injetada automaticamente.

    Returns:
        dict: Confirmação da exclusão.
    """
    jogo = db.query(Jogo).filter(Jogo.id == jogo_id).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    try:
        db.delete(jogo)
        db.commit()
        return {"message": "Jogo excluído com sucesso", "id": jogo_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao excluir jogo: {e}")


#Paginação e limitação dos resultados

@router.get("/jogos-paginados", response_model=list[dict])
def listar_jogos_paginados(
    page: int = 1,
    limit: int = 3,
    db: Session = Depends(get_db)
):
    """
    Retorna os registros de jogos de forma paginada.

    Args:
        page (int): Número da página (default: 1).
        limit (int): Quantidade máxima de registros por página (default: 10).
        db (Session): Sessão do banco de dados injetada automaticamente.

    Returns:
        list[dict]: Lista de jogos paginada.
    """
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page e limit devem ser maiores que 0.")

    offset = (page - 1) * limit
    try:
        jogos = db.query(Jogo).offset(offset).limit(limit).all()
        return [
            {
                "id": jogo.id,
                "nome": jogo.nome,
                "desenvolvedor": jogo.desenvolvedor,
                "preco": jogo.preco,
                "estoque": jogo.estoque,
                "data_lancamento": jogo.data_lancamento
            }
            for jogo in jogos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar jogos paginados: {e}")


#Filtrar jogos 
@router.get("/filtrar", response_model=list[dict])
def filtrar_jogos(
    nome: str = None,
    desenvolvedor: str = None,
    preco_min: float = None,
    preco_max: float = None,
    data_inicio: date = None,
    data_fim: date = None,
    ano_lancamento: int = None,
    db: Session = Depends(get_db)
):
    """
    Filtra jogos com base nos parâmetros fornecidos.

    Args:
        nome (str, optional): Nome do jogo.
        desenvolvedor (str, optional): Desenvolvedor do jogo.
        preco_min (float, optional): Preço mínimo.
        preco_max (float, optional): Preço máximo.
        data_inicio (date, optional): Data mínima de lançamento.
        data_fim (date, optional): Data máxima de lançamento.
        ano_lancamento (int, optional): Ano específico de lançamento.
        db (Session): Sessão do banco de dados injetada automaticamente.

    Returns:
        list[dict]: Lista de jogos que atendem aos critérios de filtragem.
    """
    query = db.query(Jogo)

    # Adiciona filtros dinamicamente com base nos parâmetros fornecidos
    if nome:
        query = query.filter(Jogo.nome.ilike(f"%{nome}%"))
    if desenvolvedor:
        query = query.filter(Jogo.desenvolvedor.ilike(f"%{desenvolvedor}%"))
    if preco_min is not None:
        query = query.filter(Jogo.preco >= preco_min)
    if preco_max is not None:
        query = query.filter(Jogo.preco <= preco_max)
    if data_inicio:
        query = query.filter(Jogo.data_lancamento >= data_inicio)
    if data_fim:
        query = query.filter(Jogo.data_lancamento <= data_fim)
    if ano_lancamento:
        query = query.filter(extract('year', Jogo.data_lancamento) == ano_lancamento)

    jogos = query.all()
    return [
        {
            "id": jogo.id,
            "nome": jogo.nome,
            "desenvolvedor": jogo.desenvolvedor,
            "preco": jogo.preco,
            "estoque": jogo.estoque,
            "data_lancamento": jogo.data_lancamento
        }
        for jogo in jogos
    ]



