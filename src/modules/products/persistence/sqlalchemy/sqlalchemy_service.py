import uuid
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.products.core.entity.product_entity import ProductEntity
from src.modules.products.core.service.product_service import ProductService


class SQLAlchemyProductService(ProductService):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_all_products(self):
        result = await self.db.execute(select(ProductEntity))
        return result.scalars().all()

    async def add_new_product(self, product_data) -> ProductEntity:
        new_product = ProductEntity(**product_data.dict())
        self.db.add(new_product)
        await self.db.commit()
        await self.db.refresh(new_product)
        return new_product

    async def get_by_id(self, product_id: uuid.UUID) -> ProductEntity:
        result = await self.db.execute(
            select(ProductEntity).where(ProductEntity.id == product_id)
        )
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product

    async def update_product(self, product_id: uuid.UUID, product_data) -> ProductEntity:
        result = await self.db.execute(
            select(ProductEntity).where(ProductEntity.id == product_id)
        )
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        for key, value in product_data.dict(exclude_unset=True).items():
            setattr(product, key, value)

        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete_product(self, product_id: uuid.UUID) -> None:
        result = await self.db.execute(
            select(ProductEntity).where(ProductEntity.id == product_id)
        )
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        await self.db.delete(product)
        await self.db.commit()
