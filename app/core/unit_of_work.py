from sqlmodel import Session

from app.producto.repository import ProductoRepository
from app.categoria.repository import CategoriaRepository
from app.ingrediente.repository import IngredienteRepository


class UnitOfWork:
    def __init__(self, session: Session) -> None:
        self._session = session
        self.productos = ProductoRepository(session)
        self.categorias = CategoriaRepository(session)
        self.ingredientes = IngredienteRepository(session)

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self._session.commit()
        else:
            self._session.rollback()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
