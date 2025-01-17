from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Plataforma, Jogo  # Modelos SQLAlchemy
from app.schemas import PlataformaCreate, PlataformaResponse  # Modelos Pydantic
from typing import List

router = APIRouter()

@router.get("/plataformas/", response_model=List[PlataformaResponse])
def listar_plataformas(db: Session = Depends(get_db)):
    return db.query(Plataforma).all()

@router.post("/plataformas/", response_model=PlataformaResponse)
def criar_plataforma(plataforma: PlataformaCreate, db: Session = Depends(get_db)):
    nova_plataforma = Plataforma(**plataforma.dict())
    db.add(nova_plataforma)
    db.commit()
    db.refresh(nova_plataforma)
    return nova_plataforma

@router.get("/plataformas/{plataforma_id}", response_model=PlataformaResponse)
def obter_plataforma(plataforma_id: int, db: Session = Depends(get_db)):
    plataforma = db.query(Plataforma).filter(Plataforma.id == plataforma_id).first()
    if not plataforma:
        raise HTTPException(status_code=404, detail="Plataforma não encontrada")
    return plataforma
