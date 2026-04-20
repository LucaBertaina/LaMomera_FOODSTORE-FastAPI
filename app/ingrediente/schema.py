from typing import Optional

from sqlmodel import SQLModel


class IngredienteBase(SQLModel):
    nombre: str
    stock: float = 0


class IngredienteCreate(IngredienteBase):
    pass


class IngredienteUpdate(SQLModel):
    nombre: Optional[str] = None
    stock: Optional[float] = None


class IngredienteRead(IngredienteBase):
    id: int
