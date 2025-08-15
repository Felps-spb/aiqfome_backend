from fastapi import HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from src.modules.auth.core.service.auth_service import AuthService
from src.modules.user.core.entity.user_entity import UserEntity
from src.modules.auth.utils.jwt import create_access_token
from passlib.context import CryptContext
from uuid import uuid4
from passlib.hash import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

class SQLAlchemyAuthService(AuthService):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def register_user(self, user_data):
        result = await self.db.execute(
            select(UserEntity).where(UserEntity.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        hashed_password = bcrypt.hash(user_data.password)

        new_user = UserEntity(
            id=uuid4(),
            username=user_data.username,
            email=user_data.email,
            password=hashed_password
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user
    
    async def authenticate_user(self, username: str, password: str):
        result = await self.db.execute(
            select(UserEntity).where(UserEntity.username == username)
        )
        user = result.scalar_one_or_none()
        
        if not user or not pwd_context.verify(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }