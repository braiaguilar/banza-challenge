from fastapi import APIRouter, HTTPException, Depends
from config.database import Session, get_db
from models.categorias import Categoria, CategoriaOut
from typing import List

router = APIRouter(
    prefix="/categorias",
    tags=["categorias"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=CategoriaOut)
def create_categoria(categoria: Categoria, db: Session = Depends(get_db)):
    categoria.nombre = categoria.nombre.strip().title()

    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

@router.get("/", response_model=List[CategoriaOut])
def get_categorias(db: Session = Depends(get_db)):
    categorias = db.query(Categoria).all()
    return categorias

@router.get("/{categoria_id}", response_model=CategoriaOut)
def get_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if categoria:
        return categoria
    else:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

@router.delete("/{categoria_id}", response_model=dict)
def delete_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if categoria:
        db.delete(categoria)
        db.commit()
        return {"message": "Categoria eliminada"}
    else:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
