from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.schemas import PetBase, PetResponse, PetDetails, PetUpdate, PetPhotoBase
from app.models import model
from app.database.connection import get_db

router = APIRouter(prefix="/pets", tags=["pets"])

@router.post("/", response_model=PetResponse, status_code=201)
async def create_pet(
    pet: PetBase, 
    foto_perfil: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Cria o pet
    db_pet = model.Pet(**pet.model_dump())
    db.add(db_pet)
    db.flush()  # Gera o ID do pet antes do commit

    # Cria o diário vazio automaticamente
    db_diario = model.Diario(conteudo="", id_pet=db_pet.id_pet)
    db.add(db_diario)

    # Cria a área de saúde automaticamente
    db_saude = model.SaudePet(id_pet=db_pet.id_pet)
    db.add(db_saude)

    # Processa a foto se fornecida
    if foto_perfil:
        if not foto_perfil.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="Apenas arquivos de imagem são permitidos"
            )

        foto_data = await foto_perfil.read()
        db_foto = model.Foto(
            foto=foto_data,
            tipo_arquivo=foto_perfil.content_type
        )
        db.add(db_foto)
        db.flush()
        db_pet.id_foto = db_foto.id_foto

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

@router.post("/{pet_id}/foto", response_model=PetPhotoBase, status_code=201) #Mas aqui tenho que gerar a resposta da foto
async def upload_foto_pet(
    pet_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    pet = db.query(model.Pet).filter(model.Pet.id_pet == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")

    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="Apenas arquivos de imagem são permitidos"
        )

    foto_data = await file.read()
    
    # Remove foto existente se houver
    if pet.id_foto:
        db.query(model.Foto).filter(model.Foto.id_foto == pet.id_foto).delete()

    # Adiciona nova foto
    db_foto = model.Foto(
        foto=foto_data,
        tipo_arquivo=file.content_type
    )
    db.add(db_foto)
    db.commit()
    db.refresh(db_foto)
    
    pet.id_foto = db_foto.id_foto
    db.commit()
    
    return {
        "id_foto": db_foto.id_foto,
        "tipo_arquivo": db_foto.tipo_arquivo
    }

@router.delete("/{pet_id}/foto", status_code=204)
def delete_foto_pet(
    pet_id: int,
    db: Session = Depends(get_db)
):
    pet = db.query(model.Pet).filter(model.Pet.id_pet == pet_id).first()
    if pet is None or pet.id_foto is None:
        raise HTTPException(status_code=404, detail="Nenhuma foto encontrada")

    db.query(model.Foto).filter(model.Foto.id_foto == pet.id_foto).delete()
    pet.id_foto = None
    db.commit()
    return

@router.get("/carrossel/{user_id}", response_model=List[dict])
def get_pets_carrossel(user_id: int, db: Session = Depends(get_db)):
    pets = db.query(
        model.Pet.id_pet,
        model.Pet.nome,
        model.Foto.foto,
        model.Foto.tipo_arquivo
    ).join(
        model.Foto, model.Pet.id_foto == model.Foto.id_foto, isouter=True
    ).filter(
        model.Pet.id_usuario == user_id
    ).all()
    
    return [{
        "id": pet.id_pet,
        "nome": pet.nome,
        "foto": pet.foto.decode('utf-8') if pet.foto else None,
        "tipo_arquivo": pet.tipo_arquivo
    } for pet in pets]