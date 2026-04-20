from typing import List, Sequence
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.core.repository import BaseRepository
from app.producto.model import Producto, ProductoCategoriaLink


class ProductoRepository(BaseRepository[Producto]):
    def __init__(self, session: Session):
        super().__init__(session, Producto)

    def get_by_id_full(self, record_id: int) -> Producto | None:
        stmt = (
            select(Producto)
            .where(
                Producto.id == record_id,
                (Producto.borrado.is_(False)) | (Producto.borrado.is_(None)),
            )
            .options(selectinload(Producto.categorias))
            .options(selectinload(Producto.ingredientes_relacionados))
        )
        return self.session.exec(stmt).first()

    def get_all_full(self, offset: int = 0, limit: int = 20) -> Sequence[Producto]:
        stmt = (
            select(Producto)
            .where((Producto.borrado.is_(False)) | (Producto.borrado.is_(None)))
            .options(selectinload(Producto.categorias))
            .options(selectinload(Producto.ingredientes_relacionados))
            .offset(offset)
            .limit(limit)
        )
        return self.session.exec(stmt).all()

    def get_por_categoria(self, categoria_id: int, offset: int = 0, limit: int = 20) -> Sequence[Producto]:
        stmt = (
            select(Producto)
            .join(ProductoCategoriaLink)
            .where(
                ProductoCategoriaLink.categoria_id == categoria_id,
                ((Producto.borrado.is_(False)) | (Producto.borrado.is_(None)))
            )
            .options(selectinload(Producto.categorias))
            .options(selectinload(Producto.ingredientes_relacionados))
            .offset(offset)
            .limit(limit)
        )
        return self.session.exec(stmt).all()
