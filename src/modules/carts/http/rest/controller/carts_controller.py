# src/modules/carts/http/rest/cart_router.py

import uuid
import logging
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database.psql import get_db
from src.modules.auth.utils.jwt import get_current_user
from src.modules.user.core.entity.user_entity import UserEntity
from src.modules.carts.http.rest.dto.carts_dto import CartCreateDTO, CartUpdateDTO, CartResponseDTO
from src.modules.carts.persistence.sqlalchemy.sqlalchemy_service import SQLAlchemyCartsService 

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Carts"])


@router.get("/carts", response_model=List[CartResponseDTO])
async def get_all_carts(db: AsyncSession = Depends(get_db), current_user: UserEntity = Depends(get_current_user)):
    cart_service = SQLAlchemyCartsService(db)
    return await cart_service.get_all_carts()

@router.post("/carts", response_model=CartResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_cart(
    cart_data: CartCreateDTO, 
    db: AsyncSession = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user)
):   
    cart_service = SQLAlchemyCartsService(db)
    new_cart = await cart_service.add_new_cart(cart_data)
    return new_cart

@router.get("/carts/{cart_id}", response_model=CartResponseDTO)
async def get_single_cart(
    cart_id: uuid.UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user)
):
    cart_service = SQLAlchemyCartsService(db)
    return await cart_service.get_by_id(cart_id)

@router.put("/carts/{cart_id}", response_model=CartResponseDTO)
async def update_cart(
    cart_id: uuid.UUID,
    cart_data: CartUpdateDTO,
    db: AsyncSession = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user)
):
    cart_service = SQLAlchemyCartsService(db)
    return await cart_service.update_cart(cart_id, cart_data)

@router.delete("/carts/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(
    cart_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user)
):
    cart_service = SQLAlchemyCartsService(db)
    await cart_service.delete_cart(cart_id)
    return None