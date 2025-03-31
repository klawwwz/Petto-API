from fastapi import FastAPI
from app.routes.users import router as users_router 

app = FastAPI()
title = "PettoAPI - API de gerenciamento de pets"
description = "API para gerenciamento de pets, com funcionalidades de cadastro, atualização e consulta de informações sobre os pets e seus donos."
version = "1.0.0"

app.include_router(users_router)
