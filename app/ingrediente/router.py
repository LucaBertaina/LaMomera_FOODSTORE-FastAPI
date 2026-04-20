from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.ingrediente import service
from app.ingrediente.schema import (
    IngredienteCreate,
    IngredienteRead,
    IngredienteUpdate,
)

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])


@router.post("/", response_model=IngredienteRead, status_code=201)
def create_ingrediente(data: IngredienteCreate, session: Session = Depends(get_session)):
    return service.create_ingrediente(session, data)


@router.get("/", response_model=List[IngredienteRead])
def list_ingredientes(session: Session = Depends(get_session)):
    return service.get_ingredientes(session)


@router.put("/{ingrediente_id}", response_model=IngredienteRead)
def update_ingrediente(
    ingrediente_id: int,
    data: IngredienteUpdate,
    session: Session = Depends(get_session),
):
    ingrediente = service.update_ingrediente(session, ingrediente_id, data)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente


@router.delete("/{ingrediente_id}", status_code=204)
def delete_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)):
    if not service.delete_ingrediente(session, ingrediente_id):
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
