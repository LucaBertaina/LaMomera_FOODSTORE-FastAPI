from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Session

from app.core.unit_of_work import UnitOfWork
from app.categoria.model import Categoria
from app.categoria.schema import CategoriaCreate, CategoriaTreeRead, CategoriaUpdate

def create_categoria(session: Session, data: CategoriaCreate) -> Categoria:
    with UnitOfWork(session) as uow:
        categoria = Categoria.model_validate(data)
        return uow.categorias.add(categoria)

def get_categorias(session: Session) -> List[Categoria]:
    with UnitOfWork(session) as uow:
        return list(uow.categorias.get_all_full())


def get_categorias_tree(session: Session) -> List[CategoriaTreeRead]:
    with UnitOfWork(session) as uow:
        categorias = list(uow.categorias.get_all_for_tree())

        nodes_by_id: dict[int, CategoriaTreeRead] = {}
        for categoria in categorias:
            nodes_by_id[categoria.id] = CategoriaTreeRead(
                id=categoria.id,
                parent_id=categoria.parent_id,
                nombre=categoria.nombre,
                descripcion=categoria.descripcion,
                imagen_url=categoria.imagen_url,
                children=[],
            )

        roots: List[CategoriaTreeRead] = []
        for node in nodes_by_id.values():
            if node.parent_id is None:
                roots.append(node)
                continue

            parent = nodes_by_id.get(node.parent_id)
            if parent is None:
                roots.append(node)
                continue

            parent.children.append(node)

        return roots

def update_categoria(session: Session, cat_id: int, data: CategoriaUpdate) -> Optional[Categoria]:
    with UnitOfWork(session) as uow:
        categoria = uow.categorias.get_by_id(cat_id)
        if not categoria:
            return None
        
        cat_data = data.model_dump(exclude_unset=True)
        for key, value in cat_data.items():
            setattr(categoria, key, value)
        
        categoria.updated_at = datetime.now(timezone.utc)
        session.add(categoria)
        
        return uow.categorias.get_by_id_full(cat_id)

def delete_categoria(session: Session, cat_id: int) -> bool:
    with UnitOfWork(session) as uow:
        categoria = uow.categorias.get_by_id(cat_id)
        if not categoria:
            return False

        uow.categorias.delete(categoria)
        
        return True