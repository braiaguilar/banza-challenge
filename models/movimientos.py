from config.database import Base
from sqlalchemy import Column, Integer, ForeignKey, String, Float, Date
from pydantic import BaseModel

class Movimiento(Base):
    __tablename__ = "movimientos"
    id = Column(Integer, primary_key=True, index=True)
    id_cuenta = Column(Integer, ForeignKey("cuentas.id"))
    tipo = Column(String)
    importe = Column(Float)
    fecha = Column(Date)

    class MovimientoOut(BaseModel):
        id: int
    # Add other fields as needed
        class Config:
            arbitrary_types_allowed = True