from config.database import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

class ClienteBase(BaseModel):
    nombre: str

class ClienteCreate(ClienteBase):
    pass

class ClienteInDB(ClienteBase):
    id: int

class ClienteOut(ClienteBase):
    id: int

    class Config:
        arbitrary_types_allowed = True
