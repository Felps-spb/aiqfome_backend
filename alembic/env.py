# env.py

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool

# 1. Importe a Base e a URL do seu arquivo de configuração central
from src.shared.database.psql import Base, DATABASE_URL 

# 2. ESSENCIAL: Importe TODOS os seus modelos aqui!
# Alembic só "enxerga" os modelos que foram importados e, consequentemente,
# registrados no `Base.metadata`.
from src.modules.user.core.entity.user_entity import UserEntity
from src.modules.products.core.entity.product_entity import ProductEntity
from src.modules.carts.core.entity.carts_entity import CartEntity
from src.modules.carts.core.entity.cartitem_entity import CartItemEntity

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Defina o target_metadata DEPOIS de importar os modelos
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Executa migrações no modo offline (gera SQL)."""
    # Usamos a URL importada do nosso código, garantindo consistência
    url = DATABASE_URL.replace("+asyncpg", "") 
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Executa migrações no modo online (direto no banco)."""
    # Usamos a URL importada do nosso código
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
                compare_type=True
            )
        )
        
        # Inicia a transação antes de rodar as migrações
        async with connection.begin():
            await connection.run_sync(lambda sync_conn: context.run_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())