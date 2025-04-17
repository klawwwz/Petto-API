from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models import model
from app.database.connection import get_db
import secrets
import string

router = APIRouter(tags=["autenticação"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/recuperar-senha")
async def recuperar_senha(email: str, db: Session = Depends(get_db)):
    user = db.query(model.Usuario).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email não encontrado")
    
    nova_senha = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
    user.senha = get_password_hash(nova_senha)
    db.commit()

    # Em produção: enviar nova_senha por email
    return {"message": "Nova senha gerada. Verifique seu email.", "nova_senha": nova_senha}
