from typing import List, Optional

from sqlmodel import Field, SQLModel

class CategoriaBase(SQLModel):
    parent_id: Optional[int] = None
    nombre: str
    descripcion: str
    imagen_url: str = ""

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(SQLModel):
    parent_id: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None

class CategoriaRead(CategoriaBase):
    id: int


class CategoriaTreeRead(CategoriaRead):
    children: List["CategoriaTreeRead"] = Field(default_factory=list)


CategoriaTreeRead.model_rebuild()
