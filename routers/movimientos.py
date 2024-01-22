from fastapi import APIRouter, Depends, HTTPException
from models.movimientos import Movimiento
from config.database import Session, get_db

router = APIRouter(
    prefix="/movimientos",
    tags=["movimientos"],
    responses={404: {"description": "Not found"}},
)

@router.post("/movimientos/")
def create_movimiento(movimiento: Movimiento, db: Session = Depends(get_db)):
    db.add(movimiento)
    db.commit()
    db.refresh(movimiento)
    return movimiento