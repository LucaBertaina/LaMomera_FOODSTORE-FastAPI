from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.categoria import service
from app.categoria.schema import CategoriaCreate, CategoriaRead, CategoriaUpdate

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.post("/", response_model=CategoriaRead, status_code=201)
def create_categoria(data: CategoriaCreate, session: Session = Depends(get_session)):
    return service.create_categoria(session, data)

@router.get("/", response_model=List[CategoriaRead])
def list_categorias(session: Session = Depends(get_session)):
    return service.get_categorias(session)

@router.put("/{cat_id}", response_model=CategoriaRead)
def update_categoria(cat_id: int, data: CategoriaUpdate, session: Session = Depends(get_session)):
    categoria = service.update_categoria(session, cat_id, data)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.delete("/{cat_id}", status_code=204)
def delete_categoria(cat_id: int, session: Session = Depends(get_session)):
    if not service.delete_categoria(session, cat_id):
        raise HTTPException(status_code=404, detail="Categoría no encontrada")