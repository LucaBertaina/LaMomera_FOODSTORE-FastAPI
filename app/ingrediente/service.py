from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import Session

from app.core.unit_of_work import UnitOfWork
from app.ingrediente.model import Ingrediente
from app.ingrediente.schema import IngredienteCreate, IngredienteUpdate


def create_ingrediente(session: Session, data: IngredienteCreate) -> Ingrediente:
    with UnitOfWork(session) as uow:
        ingrediente = Ingrediente.model_validate(data)
        return uow.ingredientes.add(ingrediente)


def get_ingredientes(session: Session) -> List[Ingrediente]:
    with UnitOfWork(session) as uow:
        return list(uow.ingredientes.get_all_full())


def update_ingrediente(
    session: Session, ingrediente_id: int, data: IngredienteUpdate
) -> Optional[Ingrediente]:
    with UnitOfWork(session) as uow:
        ingrediente = uow.ingredientes.get_by_id(ingrediente_id)
        if not ingrediente or ingrediente.borrado:
            return None

        ingrediente_data = data.model_dump(exclude_unset=True)
        for key, value in ingrediente_data.items():
            setattr(ingrediente, key, value)

        ingrediente.updated_at = datetime.now(timezone.utc)
        session.add(ingrediente)

        return uow.ingredientes.get_by_id_full(ingrediente_id)


def delete_ingrediente(session: Session, ingrediente_id: int) -> bool:
    with UnitOfWork(session) as uow:
        ingrediente = uow.ingredientes.get_by_id(ingrediente_id)
        if not ingrediente:
            return False

        uow.ingredientes.delete(ingrediente)

        return True
