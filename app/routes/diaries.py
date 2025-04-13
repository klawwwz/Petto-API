from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.models.schemas import DiaryBase
from app.models import model
from app.database.connection import get_db

router = APIRouter(prefix="/diaries", tags=["diaries"])

@router.get("/pet/{pet_id}", response_model=List[DiaryBase])
def get_pet_diaries(pet_id: int, db: Session = Depends(get_db)):
    diaries = db.query(model.Diario).filter(model.Diario.id_pet == pet_id).all()
    return diaries

@router.get("/{entry_id}")
def get_diary_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(model.Diario).filter(model.Diario.id_diario == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entrada não encontrada")
    return entry