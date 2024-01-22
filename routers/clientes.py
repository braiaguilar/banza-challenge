from fastapi import APIRouter, Depends, HTTPException
from models.clientes import Cliente, ClienteOut
from models.cuentas import Cuenta
from models.categorias import Categoria
from models.categoria_cliente import Categoria_Cliente
from config.database import Session, get_db
from typing import List

router = APIRouter(
    prefix="/clientes",
    tags=["clientes"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[ClienteOut])
def get_clientes(db: Session = Depends(get_db)):
    clientes = db.query(Cliente).all()
    return clientes

@router.get("/{cliente_id}", response_model=ClienteOut)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente:
        cliente_info = {"id": db_cliente.id, "nombre": db_cliente.nombre}

        cuentas = db.query(Cuenta).filter(Cuenta.id_cliente == cliente_id).all()
        cliente_info["cuentas"] = [{"id": cuenta.id, "saldo_usd": cuenta.get_total_usd()} for cuenta in cuentas]

        categorias = (
            db.query(Categoria)
            .join(Categoria_Cliente, Categoria.id == Categoria_Cliente.id_categoria)
            .filter(Categoria_Cliente.id_cliente == cliente_id)
            .all()
        )
        cliente_info["categorias"] = [{"id": categoria.id, "nombre": categoria.nombre} for categoria in categorias]

        return cliente_info
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

@router.get("/{cliente_id}/saldos", response_model=dict)
def get_saldos(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente:
        cuentas = db.query(Cuenta).filter(Cuenta.id_cliente == cliente_id).all()

        saldos = {}
        for cuenta in cuentas:
            saldos[cuenta.id] = {"id_cuenta": cuenta.id, "saldo_usd": cuenta.get_total_usd()}

        return saldos
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

@router.post("/", response_model=ClienteOut)
def create_cliente(cliente: Cliente, db: Session = Depends(get_db)):
    cliente.nombre = cliente.nombre.strip().title()
    
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

@router.post("/{cliente_id}/categorias/{categoria_id}", response_model=Categoria_Cliente)
def add_cliente_to_categoria(cliente_id: int, categoria_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    db_categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()

    if db_cliente and db_categoria:
        db_categoria_cliente = Categoria_Cliente(id_categoria=categoria_id, id_cliente=cliente_id)
        db.add(db_categoria_cliente)
        db.commit()
        db.refresh(db_categoria_cliente)
        return db_categoria_cliente
    elif not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    elif not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

@router.put("/{cliente_id}", response_model=ClienteOut)
def update_cliente(cliente_id: int, cliente: Cliente, db: Session = Depends(get_db)):
    nombre = cliente.nombre.strip().title()

    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente:
        db_cliente.nombre = nombre
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
@router.delete("/{cliente_id}", response_model=dict)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
        return {"message": "Cliente eliminado"}
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")