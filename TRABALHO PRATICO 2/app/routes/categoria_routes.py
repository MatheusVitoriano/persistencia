from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Categoria
from app.schemas import CategoriaRead, CategoriaCreate, CategoriaUpdate

router = APIRouter()

@router.get("/categorias/", response_model=List[CategoriaRead])
def listar_categorias(db: Session = Depends(get_db)):
    categorias = db.query(Categoria).all()
    return categorias

@router.post("/categorias/", response_model=CategoriaRead)
def criar_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    nova_categoria = Categoria(**categoria.dict())
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria

@router.put("/categorias/{categoria_id}", response_model=CategoriaRead)
def atualizar_categoria(categoria_id: int, categoria: CategoriaUpdate, db: Session = Depends(get_db)):
    categoria_db = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria_db:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    for key, value in categoria.dict(exclude_unset=True).items():
        setattr(categoria_db, key, value)
    db.commit()
    db.refresh(categoria_db)
    return categoria_db

@router.delete("/categorias/{categoria_id}")
def deletar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria_db = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria_db:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    db.delete(categoria_db)
    db.commit()
    return {"detail": "Categoria deletada com sucesso"}
