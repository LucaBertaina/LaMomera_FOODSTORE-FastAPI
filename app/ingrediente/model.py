from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship

from app.core.base_model import BaseModel
from app.producto.model import ProductoIngredienteLink

if TYPE_CHECKING:
    from app.producto.model import Producto


class Ingrediente(BaseModel, table=True):
    __tablename__ = "ingrediente"

    nombre: str = Field(index=True)
    stock: float = Field(default=0)

    productos: List["Producto"] = Relationship(
        back_populates="ingredientes_relacionados",
        link_model=ProductoIngredienteLink,
    )
