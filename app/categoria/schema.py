from typing import Optional
from sqlmodel import SQLModel

class CategoriaBase(SQLModel):
    nombre: str
    descripcion: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class CategoriaRead(CategoriaBase):
    id: int
