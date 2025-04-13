from datetime import date
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional

# --- Enums para valores fixos ---
class Sexo(str, Enum):
    M = "Macho"
    F = "Fêmea"
    I = "Indefinido"

class TipoPet(str, Enum):
    CACHORRO = "Cachorro"
    GATO = "Gato"
    PASSARO = "Pássaro"
    OUTRO = "Outro"

# --- Configuração Global ---
class BaseConfig:
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            date: lambda v: v.isoformat()
        }
    )

# --- Schemas Base ---
class UserBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(..., min_length=6, pattern="^(?=.*[A-Za-z])(?=.*\d).{6,}$")

class PetBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=45)
    raca: Optional[str] = Field(None, max_length=45)
    dataNasc: Optional[date] = Field(None, examples=["2020-01-01"])
    tipo: TipoPet
    sexo: Optional[Sexo] = None
    peso: Optional[float] = Field(None, gt=0, le=200, description="Peso em kg")
    cor: Optional[str] = Field(None, max_length=45)

    @field_validator('dataNasc', mode='before')
    @classmethod
    def parse_date(cls, value) -> Optional[date]:
        if not value:
            return None
        if isinstance(value, date):
            return value
        try:
            return date.fromisoformat(value)
        except ValueError:
            raise ValueError("Formato de data inválido. Use YYYY-MM-DD")

# --- Schemas de Diário (Somente Leitura) ---
class DiaryRead(BaseModel, BaseConfig):
    id: int
    titulo: str = Field(..., max_length=45)
    conteudo: str = Field(..., max_length=500)
    data_criacao: date
    pet_id: int
    user_id: int

    # Desabilita criação/atualização
    model_config = ConfigDict(
        extra='forbid',  # Não permite campos extras
        frozen=True  # Torna o modelo imutável
    )

# --- Outros Schemas (Eventos, Doenças, etc) ---
class EventRead(BaseModel, BaseConfig):
    id: int
    nome: str = Field(..., max_length=45)
    data: date
    pet_id: int

class DiseaseRead(BaseModel, BaseConfig):
    id: int
    nome: str = Field(..., max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)
    pet_id: int

# --- Schemas de Atualização ---
class UserUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    senha: Optional[str] = Field(None, min_length=6)

class PetUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=45)
    raca: Optional[str] = Field(None, max_length=45)
    dataNasc: Optional[date] = Field(None, examples=["2020-01-01"])
    tipo: Optional[TipoPet] = None
    sexo: Optional[Sexo] = None
    peso: Optional[float] = Field(None, gt=0, le=200)
    cor: Optional[str] = Field(None, max_length=45)

# --- Schemas de Resposta ---
class UserResponse(BaseModel, BaseConfig):
    msg: str
    nome: str

class PetResponse(BaseModel, BaseConfig):
    id: int
    nome: str
    tipo: str
    diarios: list[DiaryRead] = []  # Lista de diários (somente leitura)

class PetDetails(PetResponse):
    raca: Optional[str] = None
    dataNasc: Optional[date] = None
    sexo: Optional[str] = None
    peso: Optional[float] = None
    cor: Optional[str] = None