from typing import Sequence
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.core.repository import BaseRepository
from app.ingrediente.model import Ingrediente


class IngredienteRepository(BaseRepository[Ingrediente]):
    def __init__(self, session: Session):
        super().__init__(session, Ingrediente)

    def get_by_id_full(self, record_id: int) -> Ingrediente | None:
        stmt = (
            select(Ingrediente)
            .where(
                Ingrediente.id == record_id,
                (Ingrediente.borrado.is_(False)) | (Ingrediente.borrado.is_(None)),
            )
            .options(selectinload(Ingrediente.productos))
        )
        return self.session.exec(stmt).first()

    def get_all_full(self, offset: int = 0, limit: int = 20) -> Sequence[Ingrediente]:
        stmt = (
            select(Ingrediente)
            .where((Ingrediente.borrado.is_(False)) | (Ingrediente.borrado.is_(None)))
            .options(selectinload(Ingrediente.productos))
            .offset(offset)
            .limit(limit)
        )
        return self.session.exec(stmt).all()
