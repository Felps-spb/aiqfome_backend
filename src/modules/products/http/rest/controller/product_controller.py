import uuid
import logging
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.database.psql import get_db
from src.modules.auth.utils.jwt import get_current_user
from src.modules.user.core.entity.user_entity import UserEntity
from src.modules.products.http.rest.dto.product_dto import (
    ProductCreateDTO, ProductUpdateDTO, ProductResponseDTO
)
from src.modules.products.persistence.sqlalchemy.sqlalchemy_service import SQLAlchemyProductService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Products"])

@router.get("/products", response_model=list[ProductResponseDTO])
async def list_products(
    db: AsyncSession = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user)
):
    try:
        service = SQLAlchemyProductService(db)
        return await service.get_all_products()
    except Exception as e:
        logger.error(f"Error listing products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while fetching products."
        )

@router.post("/products", response_model=ProductResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreateDTO, 
    db: AsyncSession = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user)
):
    try:
        service = SQLAlchemyProductService(db)
        return await service.add_new_product(product_data)
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while creating the product."
        )

@router.get("/products/{product_id}", response_model=ProductResponseDTO)
async def get_product(
    product_id: uuid.UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user)
):
    try:
        service = SQLAlchemyProductService(db)
        product = await service.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        return product
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error getting product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred."
        )

@router.put("/products/{product_id}", response_model=ProductResponseDTO)
async def update_product(
    product_id: uuid.UUID, 
    product_data: ProductUpdateDTO, 
    db: AsyncSession = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user)
):
    try:
        service = SQLAlchemyProductService(db)
        updated_product = await service.update_product(product_id, product_data)
        return updated_product
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error updating product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while updating the product."
        )

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: uuid.UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user)
):
    try:
        service = SQLAlchemyProductService(db)
        deleted_count = await service.delete_product(product_id)
        return None
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error deleting product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while deleting the product."
        )