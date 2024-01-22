from fastapi import APIRouter, HTTPException, Depends
from config.database import Session, get_db
from models.cuentas import Cuenta, CuentaOut
from typing import List

router = APIRouter(
    prefix="/cuentas",
    tags=["cuentas"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=CuentaOut)
def create_cuenta(cuenta: Cuenta, db: Session = Depends(get_db)):
    db.add(cuenta)
    db.commit()
    db.refresh(cuenta)
    return cuenta

@router.get("/", response_model=List[CuentaOut])
def get_cuentas(db: Session = Depends(get_db)):
    cuentas = db.query(Cuenta).all()
    return cuentas

@router.get("/{cuenta_id}", response_model=CuentaOut)
def get_cuenta(cuenta_id: int, db: Session = Depends(get_db)):
    cuenta = db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()
    if cuenta:
        return cuenta
    else:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

@router.delete("/{cuenta_id}", response_model=dict)
def delete_cuenta(cuenta_id: int, db: Session = Depends(get_db)):
    cuenta = db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()
    if cuenta:
        db.delete(cuenta)
        db.commit()
        return {"message": "Cuenta eliminada"}
    else:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")