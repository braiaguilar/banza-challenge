from config.database import Base
from sqlalchemy import Column, Integer, ForeignKey

class Categoria_Cliente(Base):
    __tablename__ = "categoria_clientes"
    id_categoria = Column(Integer, ForeignKey("categorias.id"), primary_key=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), primary_key=True)