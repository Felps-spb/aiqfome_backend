import uuid
from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.carts.core.entity.carts_entity import CartEntity
from src.modules.carts.core.entity.cartitem_entity import CartItemEntity
from src.modules.products.core.entity.product_entity import ProductEntity
from src.modules.carts.http.rest.dto.carts_dto import CartCreateDTO, CartUpdateDTO
from src.modules.carts.core.service.carts_service import CartsService
from sqlalchemy.exc import NoResultFound

class SQLAlchemyCartsService(CartsService):

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_cart_by_id_and_user(self, cart_id: uuid.UUID, user_id: uuid.UUID):
        stmt = select(CartEntity).where(
            CartEntity.id == cart_id,
            CartEntity.user_id == user_id
        )
        result = await self.db.execute(stmt)
        cart = result.scalar_one_or_none()
        if not cart:
            raise NoResultFound(f"Cart {cart_id} not found for this user")
        return cart

    async def get_all_carts(self):
        stmt = select(CartEntity).options(
            selectinload(CartEntity.items).selectinload(CartItemEntity.product)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, cart_id: uuid.UUID):
        stmt = (
            select(CartEntity)
            .where(CartEntity.id == cart_id)
            .options(
                selectinload(CartEntity.items).selectinload(CartItemEntity.product)
            )
        )
        result = await self.db.execute(stmt)
        cart = result.scalars().first()

        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found"
            )
        return cart

    async def add_new_cart(self, cart_data: CartCreateDTO):
        product_ids = [p.product_id for p in cart_data.products]
        product_stmt = select(ProductEntity).where(ProductEntity.id.in_(product_ids))
        product_result = await self.db.execute(product_stmt)
        found_products = {p.id: p for p in product_result.scalars().all()}

        if len(found_products) != len(product_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more products not found"
            )
        
        new_cart = CartEntity(user_id=cart_data.user_id)
        self.db.add(new_cart)
        await self.db.flush()

        for item in cart_data.products:
            if item.product_id not in found_products:
                continue
            cart_item = CartItemEntity(
                cart_id=new_cart.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            self.db.add(cart_item)

        await self.db.commit()
        await self.db.refresh(new_cart)
        stmt = (
            select(CartEntity)
            .options(selectinload(CartEntity.items).selectinload(CartItemEntity.product))
            .where(CartEntity.id == new_cart.id)
        )
        result = await self.db.execute(stmt)
        cart_with_items = result.scalar_one()
        return cart_with_items

    async def update_cart(self, cart_id: uuid.UUID, cart_data: CartUpdateDTO):
        cart_to_update = await self.get_by_id(cart_id)

        delete_stmt = delete(CartItemEntity).where(CartItemEntity.cart_id == cart_to_update.id)
        await self.db.execute(delete_stmt)

        for item in cart_data.products:
            cart_item = CartItemEntity(
                cart_id=cart_to_update.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            self.db.add(cart_item)

        await self.db.commit()

        stmt = (
            select(CartEntity)
            .options(selectinload(CartEntity.items).selectinload(CartItemEntity.product))
            .where(CartEntity.id == cart_to_update.id)
        )
        result = await self.db.execute(stmt)
        updated_cart = result.scalar_one()
        return updated_cart

    async def delete_cart(self, cart_id: uuid.UUID):
        result = await self.db.execute(select(CartEntity).where(CartEntity.id == cart_id))
        cart = result.scalar_one_or_none()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        await self.db.delete(cart) 
        await self.db.commit()