from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.schemas import PetBase, PetResponse, PetDetails, PetUpdate
from app.models import model
from app.database.connection import get_db

router = APIRouter(prefix="/pets", tags=["pets"])

@router.post("/", response_model=PetResponse, status_code=201)
def create_pet(pet: PetBase, db: Session = Depends(get_db)):
    db_pet = model.Pet(**pet.model_dump())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

@router.get("/", response_model=List[PetResponse])
def read_pets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pets = db.query(model.Pet).offset(skip).limit(limit).all()
    return pets

@router.get("/{pet_id}", response_model=PetDetails)
def read_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(model.Pet).filter(model.Pet.id_pet == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return pet

@router.put("/{pet_id}", response_model=PetDetails)
def update_pet(pet_id: int, pet: PetUpdate, db: Session = Depends(get_db)):
    db_pet = db.query(model.Pet).filter(model.Pet.id_pet == pet_id).first()
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    update_data = pet.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_pet, key, value)
    
    db.commit()
    db.refresh(db_pet)
    return db_pet

@router.delete("/{pet_id}", status_code=204)
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(model.Pet).filter(model.Pet.id_pet == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    db.delete(pet)
    db.commit()
    return