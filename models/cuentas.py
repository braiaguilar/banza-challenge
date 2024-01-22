from config.database import Base, Session
from sqlalchemy import Column, Integer, ForeignKey
from models.movimientos import Movimiento
import requests

class Cuenta(Base):
    __tablename__ = "cuentas"
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"))

    def get_total_usd(self):
        try:
            response = requests.get("https://www.dolarsi.com/api/api.php?type=valoresprincipales")
            data = response.json()
            dolar_bolsa = float([item["casa"]["venta"] for item in data if item["casa"]["nombre"] == "Dolar Bolsa"][0])
        except Exception as e:
            print(f"Error al obtener la cotización del Dólar Bolsa: {e}")
            return None

        saldo_en_dolares = self.calcular_saldo_en_dolares()
        saldo_en_dolares *= dolar_bolsa

        return saldo_en_dolares