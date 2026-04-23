from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, Numeric, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import Field, Relationship, SQLModel

from app.core.base_model import BaseModel

if TYPE_CHECKING:
    from app.categoria.model import Categoria
    from app.ingrediente.model import Ingrediente

class ProductoCategoriaLink(SQLModel, table=True):
    __tablename__ = "producto_categoria"
    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categoria.id", primary_key=True)
    es_principal: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProductoIngredienteLink(SQLModel, table=True):
    __tablename__ = "producto_ingrediente"
    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    ingrediente_id: int = Field(foreign_key="ingrediente.id", primary_key=True)
    es_removible: bool = Field(default=False)

class Producto(BaseModel, table=True):
    __tablename__ = "producto"

    nombre: str = Field(sa_column=Column(String(150), nullable=False, index=True))
    descripcion: str
    precio_base: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    imagen_url: List[str] = Field(default_factory=list, sa_column=Column(ARRAY(Text), nullable=False))
    stock_cantidad: int = Field(default=0, ge=0)
    disponible: bool = Field(default=True)

    categorias: List["Categoria"] = Relationship(
        back_populates="productos",
        link_model=ProductoCategoriaLink,
    )

    ingredientes_relacionados: List["Ingrediente"] = Relationship(
        back_populates="productos",
        link_model=ProductoIngredienteLink,
    )