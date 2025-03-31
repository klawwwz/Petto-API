#aqui é pra adicionar os modelos que definem as estruturas de dados que serão usadas no banco de dados
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel): 
    nome:  str
    email: EmailStr 
    senha: str 

class PetBase(BaseModel):
    nome:     str
    raca:     str   | None = None
    dataNasc: str   | None = None #datetime / preciso ver como definir para receber uma data "YYYY-MM-DD"
    tipo:     str
    sexo:     str   | None = None #aqui preciso colocar pra ser ou só macho, ou só fêmea ou indefinido
    peso:     float | None = None
    cor:      str   | None = None

class DiaryBase(BaseModel):
    data:      str #datetime / preciso ver como definir para receber uma data "YYYY-MM-DD"
    descricao: str 
    pet_id:    int #aqui é chave estrangeira do pet
    user_id:   int #aqui é chave estrangeira do user

class EventBase(BaseModel):
    nome:   str 
    data:   str #datetime / preciso ver como definir para receber uma data "YYYY-MM-DD"   
    pet_id: str #aqui é chave estrangeira do pet

class DiseaseBase(BaseModel): #Aqui é pra parte do histórico de doenças
    nome:      str 
    descricao: str | None = None
    pet_id:    str #aqui é chave estrangeira do pet

class MedicationBase(BaseModel):
    nome:      str 
    descricao: str | None = None
    pet_id:    str #aqui é chave estrangeira do pet

class VaccineBase(BaseModel):
    nome:      str   
    descricao: str | None = None
    pet_id:    str #aqui é chave estrangeira do pet

 #Preciso das classes de atualização e de resposta
class UserUpdate(UserBase): #aqui é pra atualizar os dados do usuário
    nome:  str | None = None 
    senha: str | None = None

class PetUpdate(PetBase): #aqui é pra atualizar os dados do pet
    nome:     str   | None = None
    raca:     str   | None = None
    dataNasc: str   | None = None #datetime / preciso ver como definir para receber uma data "YYYY-MM-DD"
    tipo:     str   | None = None
    sexo:     str   | None = None #aqui preciso colocar pra ser ou só macho, ou só fêmea ou indefinido
    peso:     float | None = None 
    cor:      str   | None = None

class UserResponse(BaseModel): #aqui é pra retornar os dados do usuário
    msg: str
    nome: str #aqui é pra retornar só o nome

class PetResponse(PetBase): #aqui é pra retornar os dados do pet
    id:   int #aqui é pra retornar o id do pet
    nome: str  
    tipo: str

class PetDetails(PetResponse): #aqui é pra retornar os dados do pet com mais detalhes
    raca:     str   | None = None
    dataNasc: str   | None = None #datetime / preciso ver como definir para receber uma data "YYYY-MM-DD"
    sexo:     str   | None = None #aqui preciso colocar pra ser ou só macho, ou só fêmea ou indefinido
    peso:     float | None = None
    cor:      str   | None = None

class Config:
    orm_mode = True #aqui é pra permitir que o pydantic converta os dados do banco de dados em objetos do pydantic
    #isso é necessário pra que o pydantic consiga trabalhar com os dados do banco de dados, já que eles são armazenados em formato de dicionário
    #e não em formato de objeto.




