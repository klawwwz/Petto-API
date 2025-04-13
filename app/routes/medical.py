from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.schemas import MedicationBase, VaccineBase, DiseaseBase
from app.models import model
from app.database.connection import get_db

router = APIRouter(prefix="/medical", tags=["medical"])

# Rotas para Medicamentos
@router.post("/medications/", status_code=201)
def create_medication(med: MedicationBase, db: Session = Depends(get_db)):
    db_med = model.Medicamento(**med.model_dump())
    db.add(db_med)
    db.commit()
    db.refresh(db_med)
    return {"message": "Medicação registrada", "id": db_med.id_med}

@router.get("/medications/pet/{pet_id}", response_model=List[MedicationBase])
def get_pet_medications(pet_id: int, db: Session = Depends(get_db)):
    meds = db.query(model.Medicamento).filter(model.Medicamento.pet_id == pet_id).all()
    return meds

# Rotas para Vacinas
@router.post("/vaccines/", status_code=201)
def create_vaccine(vaccine: VaccineBase, db: Session = Depends(get_db)):
    db_vaccine = model.Vacina(**vaccine.model_dump())
    db.add(db_vaccine)
    db.commit()
    db.refresh(db_vaccine)
    return {"message": "Vacina registrada", "id": db_vaccine.id_vac}

@router.get("/vaccines/pet/{pet_id}", response_model=List[VaccineBase])
def get_pet_vaccines(pet_id: int, db: Session = Depends(get_db)):
    vaccines = db.query(model.Vacina).filter(model.Vacina.pet_id == pet_id).all()
    return vaccines

# Rotas para Histórico de Doenças
@router.post("/diseases/", status_code=201)
def create_disease(disease: DiseaseBase, db: Session = Depends(get_db)):
    db_disease = model.Historico(**disease.model_dump())
    db.add(db_disease)
    db.commit()
    db.refresh(db_disease)
    return {"message": "Doença registrada", "id": db_disease.id_his}

@router.get("/diseases/pet/{pet_id}", response_model=List[DiseaseBase])
def get_pet_diseases(pet_id: int, db: Session = Depends(get_db)):
    diseases = db.query(model.Historico).filter(model.Historico.pet_id == pet_id).all()
    return diseases