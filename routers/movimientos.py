from fastapi import APIRouter, Depends, HTTPException
from models.movimientos import Movimiento, MovimientoOut
from models.cuentas import Cuenta
from config.database import Session, get_db
from typing import List

router = APIRouter(
    prefix="/movimientos",
    tags=["movimientos"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{movimiento_id}", response_model=MovimientoOut)
def get_movimiento(movimiento_id: int, db: Session = Depends(get_db)):
    movimiento = db.query(Movimiento).filter(Movimiento.id == movimiento_id).first()
    if movimiento:
        return movimiento
    else:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

@router.post("/", response_model=MovimientoOut)
def create_movimiento(movimiento: Movimiento, db: Session = Depends(get_db)):
    db_cuenta = db.query(Cuenta).filter(Cuenta.id == movimiento.id_cuenta).first()

    movimiento.tipo = movimiento.tipo.strip().title()

    if movimiento.tipo not in ["Ingreso", "Egreso"]:
        raise HTTPException(status_code=400, detail="Tipo de movimiento inválido")

    if not db_cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    if movimiento.tipo == "Egreso" and movimiento.importe > db_cuenta.get_total_usd():
        raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar el Egreso")

    db.add(movimiento)
    db.commit()
    db.refresh(movimiento)

    return movimiento

@router.delete("/{movimiento_id}", response_model=dict)
def delete_movimiento(movimiento_id: int, db: Session = Depends(get_db)):
    movimiento = db.query(Movimiento).filter(Movimiento.id == movimiento_id).first()
    if movimiento:
        db.delete(movimiento)
        db.commit()
        return {"message": "Movimiento eliminado"}
    else:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")