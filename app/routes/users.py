
from http import HTTPStatus
from fastapi import APIRouter, status
from app.models.schemas import *


router = APIRouter(prefix= "/users")

@router.post("/create-user", status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(user: UserBase):
    return {"msg": "Usuario criado com sucesso", "nome": user.nome}

