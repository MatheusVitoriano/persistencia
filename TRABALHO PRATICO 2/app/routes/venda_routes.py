from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Venda  # Modelo SQLAlchemy
from app.schemas import VendaCreate, VendaResponse  # Modelos Pydantic
from typing import List

router = APIRouter()

@router.get("/vendas/", response_model=List[VendaResponse])
def listar_vendas(db: Session = Depends(get_db)):
    return db.query(Venda).all()

@router.post("/vendas/", response_model=VendaResponse)
def criar_venda(venda: VendaCreate, db: Session = Depends(get_db)):
    nova_venda = Venda(**venda.dict())
    db.add(nova_venda)
    db.commit()
    db.refresh(nova_venda)
    return nova_venda

@router.get("/vendas/{venda_id}", response_model=VendaResponse)
def obter_venda(venda_id: int, db: Session = Depends(get_db)):
    venda = db.query(Venda).filter(Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda
