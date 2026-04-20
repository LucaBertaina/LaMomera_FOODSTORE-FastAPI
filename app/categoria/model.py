from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship, SQLModel

from app.core.base_model import BaseModel
from app.producto.model import ProductoCategoriaLink

if TYPE_CHECKING:
    from app.producto.model import Producto

class Categoria(BaseModel, table=True):
    __tablename__ = "categoria"

    nombre: str = Field(index=True)
    descripcion: str

    productos: List["Producto"] = Relationship(
        back_populates="categorias",
        link_model=ProductoCategoriaLink
    )