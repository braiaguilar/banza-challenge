from config.database import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

    class CategoriaOut(BaseModel):
        id: int
        nombre: str

        class Config:
            arbitrary_types_allowed = True