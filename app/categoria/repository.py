from typing import Sequence
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.core.repository import BaseRepository
from app.categoria.model import Categoria


class CategoriaRepository(BaseRepository[Categoria]):
    def __init__(self, session: Session):
        super().__init__(session, Categoria)

    def get_by_id_full(self, record_id: int) -> Categoria | None:
        stmt = (
            select(Categoria)
            .where(
                Categoria.id == record_id,
                (Categoria.borrado.is_(False)) | (Categoria.borrado.is_(None)),
            )
            .options(selectinload(Categoria.productos))
        )
        return self.session.exec(stmt).first()

    def get_all_full(self, offset: int = 0, limit: int = 20) -> Sequence[Categoria]:
        stmt = (
            select(Categoria)
            .where((Categoria.borrado.is_(False)) | (Categoria.borrado.is_(None)))
            .options(selectinload(Categoria.productos))
            .offset(offset)
            .limit(limit)
        )
        return self.session.exec(stmt).all()
