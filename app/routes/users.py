
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.schemas import UserBase, UserResponse, UserUpdate
from app.models import model
from app.database.connection import get_db


router = APIRouter(prefix= "/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    # Verifica se email já existe
    db_user = db.query(model.Usuario).filter(model.Usuario.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    db_user = model.Usuario(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "Usuário criado com sucesso", "nome": db_user.nome}

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(model.Usuario).filter(model.Usuario.id_usuario == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"msg": "Usuário encontrado", "nome": user.nome}

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(model.Usuario).filter(model.Usuario.id_usuario == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return {"msg": "Usuário atualizado", "nome": db_user.nome}

@router.get("/{user_id}/pets", response_model=list)
def get_user_pets(user_id: int, db: Session = Depends(get_db)):
    pets = db.query(model.Pet).filter(model.Pet.id_usuario == user_id).all()
    return pets

