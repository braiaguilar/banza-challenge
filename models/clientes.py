from config.database import Base
from sqlalchemy import Column, Integer, String

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)