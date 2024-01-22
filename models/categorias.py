from config.database import Base
from sqlalchemy import Column, Integer, String

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)