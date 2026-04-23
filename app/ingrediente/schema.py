from typing import Optional

from sqlmodel import SQLModel


class IngredienteBase(SQLModel):
    nombre: str
    descripcion: str
    es_alergeno: bool = False


class IngredienteCreate(IngredienteBase):
    pass


class IngredienteUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    es_alergeno: Optional[bool] = None


class IngredienteRead(IngredienteBase):
    id: int
