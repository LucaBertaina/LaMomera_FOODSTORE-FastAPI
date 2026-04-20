from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.producto import service
from app.producto.schema import (
    ProductoCategoriaAssign,
    ProductoCreate,
    ProductoIngredienteAssign,
    ProductoReadFull,
    ProductoUpdate,
)

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/", response_model=ProductoReadFull, status_code=201)
def create_producto(data: ProductoCreate, session: Session = Depends(get_session)):
    return service.create_producto(session, data)

@router.get("/", response_model=List[ProductoReadFull])
def list_productos(session: Session = Depends(get_session)):
    return service.get_productos(session)

@router.get("/categorias/{categoria_id}", response_model=List[ProductoReadFull])
def get_productos_por_categoria(categoria_id: int, session: Session = Depends(get_session)):
    return service.get_productos_por_categoria(session, categoria_id)

@router.put("/{prod_id}", response_model=ProductoReadFull)
def update_producto(prod_id: int, data: ProductoUpdate, session: Session = Depends(get_session)):
    producto = service.update_producto(session, prod_id, data)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.delete("/{prod_id}", status_code=204)
def delete_producto(prod_id: int, session: Session = Depends(get_session)):
    if not service.delete_producto(session, prod_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")

@router.post("/{prod_id}/categorias", response_model=ProductoReadFull)
def assign_categoria(prod_id: int, body: ProductoCategoriaAssign, session: Session = Depends(get_session)):
    producto = service.add_categoria_to_producto(session, prod_id, body.categoria_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto o Categoría no encontrados")
    return producto


@router.delete("/{prod_id}/categorias/{categoria_id}", status_code=204)
def remove_categoria_from_producto(
    prod_id: int,
    categoria_id: int,
    session: Session = Depends(get_session),
):
    if not service.remove_categoria_from_producto(session, prod_id, categoria_id):
        raise HTTPException(status_code=404, detail="Producto, Categoría o relación no encontrados")


@router.post("/{prod_id}/ingredientes", response_model=ProductoReadFull)
def assign_ingrediente(
    prod_id: int,
    body: ProductoIngredienteAssign,
    session: Session = Depends(get_session),
):
    producto = service.add_ingrediente_to_producto(session, prod_id, body.ingrediente_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto o Ingrediente no encontrados")
    return producto