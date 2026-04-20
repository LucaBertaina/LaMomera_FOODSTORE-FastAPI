from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Session, select

from app.core.unit_of_work import UnitOfWork
from app.producto.model import Producto, ProductoCategoriaLink, ProductoIngredienteLink
from app.categoria.model import Categoria
from app.ingrediente.model import Ingrediente
from app.producto.schema import ProductoCreate, ProductoUpdate

def create_producto(session: Session, data: ProductoCreate) -> Producto:
    with UnitOfWork(session) as uow:
        categoria_ids = data.categoria_ids
        
        producto_data = data.model_dump(exclude={"categoria_ids"})
        producto = Producto.model_validate(producto_data)
        producto = uow.productos.add(producto)
        
        for cat_id in categoria_ids:
            categoria = uow.categorias.get_by_id(cat_id)
            if categoria and not categoria.borrado:
                link = ProductoCategoriaLink(producto_id=producto.id, categoria_id=cat_id)
                session.add(link)
        
        return uow.productos.get_by_id_full(producto.id)

def get_productos(session: Session) -> List[Producto]:
    with UnitOfWork(session) as uow:
        return list(uow.productos.get_all_full())

def get_productos_por_categoria(session: Session, categoria_id: int) -> List[Producto]:
    with UnitOfWork(session) as uow:
        return list(uow.productos.get_por_categoria(categoria_id))

def add_categoria_to_producto(session: Session, prod_id: int, cat_id: int) -> Optional[Producto]:
    with UnitOfWork(session) as uow:
        producto = uow.productos.get_by_id(prod_id)
        categoria = uow.categorias.get_by_id(cat_id)
        
        if not producto or not categoria:
            return None
        if producto.borrado or categoria.borrado:
            return None

        existing = session.exec(select(ProductoCategoriaLink).where(
            ProductoCategoriaLink.producto_id == prod_id,
            ProductoCategoriaLink.categoria_id == cat_id
        )).first()

        if not existing:
            link = ProductoCategoriaLink(producto_id=prod_id, categoria_id=cat_id)
            session.add(link)

        return uow.productos.get_by_id_full(prod_id)


def remove_categoria_from_producto(
    session: Session, prod_id: int, cat_id: int
) -> bool:
    with UnitOfWork(session) as uow:
        producto = uow.productos.get_by_id(prod_id)
        categoria = uow.categorias.get_by_id(cat_id)

        if not producto or not categoria:
            return False

        link = session.exec(
            select(ProductoCategoriaLink).where(
                ProductoCategoriaLink.producto_id == prod_id,
                ProductoCategoriaLink.categoria_id == cat_id,
            )
        ).first()

        if not link:
            return False

        session.delete(link)

        return True


def add_ingrediente_to_producto(
    session: Session, prod_id: int, ingrediente_id: int
) -> Optional[Producto]:
    with UnitOfWork(session) as uow:
        producto = uow.productos.get_by_id(prod_id)
        ingrediente = uow.ingredientes.get_by_id(ingrediente_id)

        if not producto or not ingrediente:
            return None
        if producto.borrado or ingrediente.borrado:
            return None

        existing = session.exec(
            select(ProductoIngredienteLink).where(
                ProductoIngredienteLink.producto_id == prod_id,
                ProductoIngredienteLink.ingrediente_id == ingrediente_id,
            )
        ).first()

        if not existing:
            link = ProductoIngredienteLink(
                producto_id=prod_id,
                ingrediente_id=ingrediente_id,
            )
            session.add(link)

        return uow.productos.get_by_id_full(prod_id)

def update_producto(session: Session, prod_id: int, data: ProductoUpdate) -> Optional[Producto]:
    with UnitOfWork(session) as uow:
        producto = uow.productos.get_by_id(prod_id)
        if not producto:
            return None

        prod_data = data.model_dump(exclude_unset=True)
        for key, value in prod_data.items():
            setattr(producto, key, value)

        producto.updated_at = datetime.now(timezone.utc)
        session.add(producto)

        return uow.productos.get_by_id_full(prod_id)

def delete_producto(session: Session, prod_id: int) -> bool:
    with UnitOfWork(session) as uow:
        producto = uow.productos.get_by_id(prod_id)
        if not producto:
            return False

        uow.productos.delete(producto)

        return True