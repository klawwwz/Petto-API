from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.schemas import SaudePetResponse, SaudePetUpdate
from app.models import model
from app.database.connection import get_db
from sqlalchemy.sql import func

router = APIRouter(prefix="/medical", tags=["medical"])

@router.get("/pet/{pet_id}", response_model=SaudePetResponse)
def get_saude_pet(pet_id: int, db: Session = Depends(get_db)):
    saude = db.query(model.SaudePet).filter(model.SaudePet.pet_id == pet_id).first()
    if not saude:
        raise HTTPException(status_code=404, detail="Registro de saúde não encontrado")
    return saude

@router.patch("/pet/{pet_id}", response_model=SaudePetResponse)
def update_saude_pet(
    pet_id: int,
    update: SaudePetUpdate,
    db: Session = Depends(get_db)
):
    saude = db.query(model.SaudePet).filter(model.SaudePet.pet_id == pet_id).first()
    if not saude:
        saude = model.SaudePet(pet_id=pet_id)
        db.add(saude)
    
    # Atualiza apenas os campos fornecidos, acumulando texto
    if update.vacinas is not None:
        saude.vacinas = f"{saude.vacinas}\n{update.vacinas}".strip()
    if update.medicamentos is not None:
        saude.medicamentos = f"{saude.medicamentos}\n{update.medicamentos}".strip()
    if update.doencas is not None:
        saude.doencas = f"{saude.doencas}\n{update.doencas}".strip()
    
    saude.ultima_atualizacao = func.now()
    db.commit()
    db.refresh(saude)
    return saude