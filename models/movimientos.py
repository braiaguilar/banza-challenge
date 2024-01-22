from config.database import Base
from sqlalchemy import Column, Integer, ForeignKey, String, Float, Date

class Movimiento(Base):
    __tablename__ = "movimientos"
    id = Column(Integer, primary_key=True, index=True)
    id_cuenta = Column(Integer, ForeignKey("cuentas.id"))
    tipo = Column(String)
    importe = Column(Float)
    fecha = Column(Date)