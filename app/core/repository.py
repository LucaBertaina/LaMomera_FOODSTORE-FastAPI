from datetime import datetime, timezone
from typing import Generic, TypeVar, Type, Sequence

from sqlmodel import Session, SQLModel, select

ModelT = TypeVar("ModelT", bound=SQLModel)


class BaseRepository(Generic[ModelT]):
    def __init__(self, session: Session, model: Type[ModelT]) -> None:
        self.session = session
        self.model = model

    def get_by_id(self, record_id: int) -> ModelT | None:
        stmt = select(self.model).where(
            self.model.id == record_id,
            (self.model.borrado.is_(False)) | (self.model.borrado.is_(None)),
        )
        return self.session.exec(stmt).first()

    def get_all(self, offset: int = 0, limit: int = 20) -> Sequence[ModelT]:
        return self.session.exec(
            select(self.model)
            .where((self.model.borrado.is_(False)) | (self.model.borrado.is_(None)))
            .offset(offset)
            .limit(limit)
        ).all()

    def add(self, instance: ModelT) -> ModelT:
        self.session.add(instance)
        self.session.flush()
        self.session.refresh(instance)
        return instance

    def delete(self, instance: ModelT) -> None:
        now = datetime.now(timezone.utc)
        instance.borrado = True
        instance.deleted_at = now
        instance.updated_at = now
        self.session.add(instance)
        self.session.flush()
