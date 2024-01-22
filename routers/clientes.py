from fastapi import APIRouter, Depends, HTTPException
from models.clientes import Cliente
from config.database import Session, get_db

router = APIRouter(
    prefix="/clientes",
    tags=["clientes"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_cliente(cliente: Cliente, db: Session = Depends(get_db)):
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

@router.put("/{cliente_id}")
def update_cliente(cliente_id: int, cliente: Cliente, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente:
        db_cliente.nombre = cliente.nombre
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")