#Aqui fica os modelos do banco de dados
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Blob
from sqlalchemy.orm import relationship
from database import Base

class Usuario (Base):
    __tablename__ = "usuario"
    id_usuario = Column(Integer, primary_key=True)
    email = Column(String(255))
    nome = Column(String(100))
    senha = Column(String(45))

# Área de Saúde

class Medicamentos (Base):
    __tablename__ = "medicamentos"
    id_med = Column(Integer, primary_key=True)
    conteudo = Column(String(500))

class Vacinacao (Base):
    __tablename__ = "vacinacao"
    id_vac = Column(Integer, primary_key=True)
    conteudo = Column(String(500))

class Historico (Base):
    __tablename__ = "historico"
    id_his = Column(Integer, primary_key=True)
    conteudo = Column(Integer, primary_key=True)

class Foto (Base):
    __tablename__ = "foto"
    id_foto = Column(Integer, primary_key=True)
    foto = Column(Blob)

class Pet (Base):
    __tablename__ = "pet"
    id_pet = Column(Integer, primary_key=True)
    nome = Column(String(45))
    data_nascimento = Column(Date)
    tipo = Column(String(45))
    cor = Column(String(45))
    peso = Column(String(10,2))
    raca = Column(String(45))
    sexo = Column(String(45))
    id_foto = Column(Integer, ForeignKey("foto.id_foto"))
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    id_med = Column(Integer, ForeignKey("medicamentos.id_med"))
    id_vac = Column(Integer, ForeignKey("vacinacao.id_vac"))
    id_his = Column(Integer, ForeignKey("historico.id_his"))
    #Falta terminar a ultima parte
    #CONSTRAINT pk_pet PRIMARY KEY (id_pet),
    #CONSTRAINT fk_pet_foto FOREIGN KEY (id_foto)
    #REFERENCES foto (id_foto) ON DELETE CASCADE ON UPDATE CASCADE,
    #CONSTRAINT fk_pet_usuario FOREIGN KEY (id_usuario)
    #REFERENCES usuario (id_usuario) ON DELETE CASCADE ON UPDATE CASCADE,
    #CONSTRAINT fk_pet_medicamentos FOREIGN KEY (id_med)
    #REFERENCES medicamentos (id_med) ON DELETE CASCADE ON UPDATE CASCADE,
    #CONSTRAINT fk_pet_vacinacao FOREIGN KEY (id_vac)
    #REFERENCES vacinacao (id_vac) ON DELETE CASCADE ON UPDATE CASCADE,
    #CONSTRAINT fk_pet_historico FOREIGN KEY (id_his)
    #REFERENCES historico (id_his) ON DELETE CASCADE ON UPDATE CASCADE 

class Diario (Base):
    __tablename__ = "diario"
    id_diario = Column(Integer, primary_key=True)
    titulo = Column(String(45))
    conteudo = Column(String(500))
    id_pet = Column(Integer, ForeignKey("pet.id_pet"))
    #CONSTRAINT pk_diario PRIMARY KEY (id_diario),
    #CONSTRAINT fk_diario_pet FOREIGN KEY (id_pet)
    #REFERENCES pet (id_pet) ON DELETE CASCADE ON UPDATE CASCADE
#Tela de Diário


