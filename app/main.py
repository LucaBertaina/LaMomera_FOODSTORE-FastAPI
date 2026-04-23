from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlmodel import SQLModel

from app.core.database import engine

from app.categoria.model import Categoria
from app.producto.model import Producto, ProductoCategoriaLink, ProductoIngredienteLink
from app.ingrediente.model import Ingrediente

from app.categoria.router import router as categoria_router
from app.producto.router import router as producto_router
from app.ingrediente.router import router as ingrediente_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)

    with engine.begin() as connection:
        for table_name in ("categoria", "ingrediente", "producto"):
            connection.execute(
                text(
                    f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS borrado BOOLEAN NOT NULL DEFAULT FALSE"
                )
            )
            connection.execute(
                text(
                    f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP WITH TIME ZONE"
                )
            )

        connection.execute(
            text(
                "ALTER TABLE producto ADD COLUMN IF NOT EXISTS ingredientes VARCHAR NOT NULL DEFAULT ''"
            )
        )

        connection.execute(
            text(
                "ALTER TABLE producto ADD COLUMN IF NOT EXISTS stock_cantidad INTEGER NOT NULL DEFAULT 0"
            )
        )

        connection.execute(
            text(
                "ALTER TABLE categoria ADD COLUMN IF NOT EXISTS parent_id BIGINT REFERENCES categoria(id)"
            )
        )
        connection.execute(
            text(
                "ALTER TABLE categoria ADD COLUMN IF NOT EXISTS imagen_url TEXT NOT NULL DEFAULT ''"
            )
        )

        connection.execute(
            text(
                "ALTER TABLE ingrediente ADD COLUMN IF NOT EXISTS descripcion TEXT NOT NULL DEFAULT ''"
            )
        )
        connection.execute(
            text(
                "ALTER TABLE ingrediente ADD COLUMN IF NOT EXISTS es_alergeno BOOLEAN NOT NULL DEFAULT FALSE"
            )
        )

        connection.execute(
            text(
                "ALTER TABLE producto_categoria ADD COLUMN IF NOT EXISTS es_principal BOOLEAN NOT NULL DEFAULT FALSE"
            )
        )
        connection.execute(
            text(
                "ALTER TABLE producto_categoria ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()"
            )
        )

        connection.execute(
            text(
                "ALTER TABLE producto_ingrediente ADD COLUMN IF NOT EXISTS es_removible BOOLEAN NOT NULL DEFAULT FALSE"
            )
        )

    yield

app = FastAPI(
    title="TP Integrador - FastAPI & SQLModel",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(ingrediente_router)