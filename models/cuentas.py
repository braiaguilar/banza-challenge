from config.database import Base, Session
from sqlalchemy import Column, Integer, ForeignKey
from models.movimientos import Movimiento
import requests
from pydantic import BaseModel

class Cuenta(Base):
    __tablename__ = "cuentas"
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"))

    def get_total_usd(self, db: Session):
        movimientos = (
                db.query(Movimiento)
                .filter(Movimiento.id_cuenta == self.id)
                .all()
            )
        saldo_pesos = sum([movimiento.importe if movimiento.tipo == "Ingreso" else -movimiento.importe for movimiento in movimientos])
        
        try:
            response = requests.get("https://www.dolarsi.com/api/api.php?type=valoresprincipales")
            data = response.json()
            dolar_bolsa = float([item["casa"]["venta"] for item in data if item["casa"]["nombre"] == "Dolar Bolsa"][0])
        except Exception as e:
            print(f"Error al obtener la cotización del Dólar Bolsa: {e}")
            return None

        saldo_dolares = saldo_pesos / dolar_bolsa

        return saldo_dolares
    
    class CuentaOut(BaseModel):
        id: int

        class Config:
            arbitrary_types_allowed = True