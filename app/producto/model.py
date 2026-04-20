from typing import TYPE_CHECKING, List
from sqlalchemy import Column, JSON
from sqlmodel import Field, Relationship, SQLModel

from app.core.base_model import BaseModel

if TYPE_CHECKING:
    from app.categoria.model import Categoria
    from app.ingrediente.model import Ingrediente

class ProductoCategoriaLink(SQLModel, table=True):
    __tablename__ = "producto_categoria"
    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categoria.id", primary_key=True)


class ProductoIngredienteLink(SQLModel, table=True):
    __tablename__ = "producto_ingrediente"
    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    ingrediente_id: int = Field(foreign_key="ingrediente.id", primary_key=True)

class Producto(BaseModel, table=True):
    __tablename__ = "producto"

    nombre: str = Field(index=True)
    descripcion: str
    precio_base: str
    imagen_url: List[str] = Field(default=[], sa_column=Column(JSON))
    disponible: bool = Field(default=True)
    ingredientes: str = Field(default="")

    categorias: List["Categoria"] = Relationship(
        back_populates="productos",
        link_model=ProductoCategoriaLink,
    )

    ingredientes_relacionados: List["Ingrediente"] = Relationship(
        back_populates="productos",
        link_model=ProductoIngredienteLink,
    )