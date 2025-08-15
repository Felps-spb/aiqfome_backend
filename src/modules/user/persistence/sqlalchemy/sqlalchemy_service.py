from fastapi import HTTPException, status
from src.modules.user.core.service.user_service import UserService
from src.modules.user.core.entity.user_entity import UserEntity
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class SQLAlchemyUserService(UserService):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_all_users(self):
        result = await self.db.execute(select(UserEntity))
        users = result.scalars().all()
        return users

    async def get_user_by_id(self, user_id: int):
        result = await self.db.execute(
            select(UserEntity).where(UserEntity.id == user_id)
        )
        user = result.scalar_one_or_none()
    
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "password": user.password
        }

    async def update_user(self, user_id: str, user_data) -> None:
        result = await self.db.execute(
            select(UserEntity).where(UserEntity.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        for key, value in user_data.dict().items():
            setattr(user, key, value)
        await self.db.commit()
        await self.db.refresh(user)
        return {
            "id": user.id,
            "username":user.username,
            "email": user.email,
        }

    async def delete_user(self, user_id: int) -> None:
        result = await self.db.execute(
            select(UserEntity).where(UserEntity.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        await self.db.delete(user)
        await self.db.commit()