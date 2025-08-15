from fastapi import APIRouter, Depends, HTTPException, status
from src.modules.user.core.entity.user_entity import UserEntity
from src.modules.user.persistence.sqlalchemy.sqlalchemy_service import SQLAlchemyUserService
from src.modules.user.http.rest.dto.user_dto import UserUpdateDTO, UserResponseDTO
from src.modules.auth.utils.jwt import get_current_user
from src.shared.database.psql import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Users"])

@router.get("/users")
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user)
):
    try:
        user_service = SQLAlchemyUserService(db)
        users = await user_service.get_all_users()
        return users
    except Exception as e:
        logger.error(f"Error fetching all users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while fetching users."
        )

@router.get("/users/{user_id}", response_model=UserResponseDTO)
async def get_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user)
):
    try:
        user_service = SQLAlchemyUserService(db)
        user = await user_service.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return user
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred."
        )

@router.put("/users/{user_id}", response_model=UserResponseDTO)
async def update_user(
    user_id: uuid.UUID,
    user_data: UserUpdateDTO,
    db: AsyncSession = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user)
): 
    try:
        user_service = SQLAlchemyUserService(db)
        updated_user = await user_service.update_user(user_id, user_data)

        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return updated_user
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while updating the user."
        )

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user)
):    
    try:
        user_service = SQLAlchemyUserService(db)
        deleted = await user_service.delete_user(user_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
            
        return {"detail": "User deleted successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while deleting the user."
        )