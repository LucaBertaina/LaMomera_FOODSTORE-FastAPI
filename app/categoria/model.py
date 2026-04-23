from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

from app.core.base_model import BaseModel
from app.producto.model import ProductoCategoriaLink

if TYPE_CHECKING:
    from app.producto.model import Producto

class Categoria(BaseModel, table=True):
    __tablename__ = "categoria"

    parent_id: int | None = Field(default=None, foreign_key="categoria.id")
    nombre: str = Field(sa_column=Column(String(100), nullable=False, unique=True, index=True))
    descripcion: str
    imagen_url: str = Field(default="")

    parent: Optional["Categoria"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Categoria.id"},
    )
    children: List["Categoria"] = Relationship(back_populates="parent")

    productos: List["Producto"] = Relationship(
        back_populates="categorias",
        link_model=ProductoCategoriaLink
    )