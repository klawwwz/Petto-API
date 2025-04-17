#Aqui fica os modelos do banco de dados
from sqlalchemy import  BLOB, Column, Date, ForeignKey, Integer, Numeric, String, Text, LargeBinary
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Usuario (Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False) 
    nome = Column(String(100))
    senha = Column(String(45))

class Foto(Base):
    __tablename__ = "fotos_perfil"
    
    id_foto = Column(Integer, primary_key=True, autoincrement=True)
    foto = Column(LargeBinary, nullable=False)  # Armazena os bytes da imagem
    tipo_arquivo = Column(String(50), nullable=False)  # Ex: 'image/jpeg'
    data_upload = Column(Date, server_default=func.now())

class Medicamento (Base):
    __tablename__ = "medicamentos"
    id_med = Column(Integer, primary_key=True)
    conteudo = Column(String(500))

class Vacina (Base):
    __tablename__ = "vacinas"
    id_vac = Column(Integer,  primary_key=True)
    conteudo = Column(String(500))

class Historico (Base):
    __tablename__ = "historicos"
    id_his = Column(Integer,  primary_key=True)
    conteudo = Column(String(500))
 
class Foto (Base):
    __tablename__ = "fotos" 
    id_foto = Column(Integer, primary_key=True)
    foto = Column(BLOB, nullable=False)

class Pet (Base):
    __tablename__ = "pets"
    id_pet = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(45), nullable=False)
    data_nascimento = Column(Date, nullable=True)
    tipo = Column(String(45), nullable=False)
    cor = Column(String(45), nullable=True)
    peso = Column(Numeric(10,2))
    raca = Column(String(45))
    sexo = Column(String(45))
    id_foto = Column(Integer, ForeignKey("fotos.id_foto", ondelete="cascade", onupdate="cascade"))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="cascade", onupdate="cascade"))
    id_med = Column(Integer, ForeignKey("medicamentos.id_med", ondelete="cascade", onupdate="cascade"))
    id_vac = Column(Integer, ForeignKey("vacinas.id_vac", ondelete="cascade", onupdate="cascade"))
    id_his = Column(Integer, ForeignKey("historicos.id_his", ondelete="cascade", onupdate="cascade"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.diarios = [Diario(titulo="Diário Inicial")] 
    
    usuario = relationship("Usuario", backref="pets")
    medicamentos = relationship("Medicamento", backref="pets")
    vacinacao = relationship("Vacina", backref="pets")
    historico = relationship("Historico", backref="pets")
    foto = relationship("Foto", backref="pets")

class Diario(Base):
    __tablename__ = "diarios"
    id_diario = Column(Integer, primary_key=True, autoincrement=True)
    conteudo = Column(Text, default="")
    id_pet = Column(Integer, ForeignKey("pets.id_pet", ondelete="CASCADE"), unique=True)

    pet = relationship("Pet", backref="diario", uselist=False)

    # Propriedade para obter o título dinâmico
    @property
    def titulo(self):
        return f"Diário de {self.pet.nome}" if self.pet else "Diário"
    


