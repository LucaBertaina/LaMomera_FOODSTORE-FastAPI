from typing import List, Optional
from sqlmodel import SQLModel
from app.categoria.schema import CategoriaRead
from app.ingrediente.schema import IngredienteRead

class ProductoBase(SQLModel):
    nombre: str
    descripcion: str
    precio_base: str
    imagen_url: List[str] = []
    disponible: bool = True
    ingredientes: str = ""

class ProductoCreate(ProductoBase):
    categoria_ids: List[int] = []

class ProductoUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_base: Optional[str] = None
    imagen_url: Optional[List[str]] = None
    disponible: Optional[bool] = None
    ingredientes: Optional[str] = None

class ProductoRead(ProductoBase):
    id: int

class ProductoReadFull(ProductoRead):
    categorias: List[CategoriaRead] = []
    ingredientes_relacionados: List[IngredienteRead] = []

class ProductoCategoriaAssign(SQLModel):
    categoria_id: int


class ProductoIngredienteAssign(SQLModel):
    ingrediente_id: int