from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.auth.http.rest.dto.user_create_dto import UserCreateDTO
from src.modules.auth.persistence.sqlalchemy.sqlalchemy_service import SQLAlchemyAuthService
from src.shared.database.psql import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register_user(
    user_data: UserCreateDTO,
    db: AsyncSession = Depends(get_db)
):
    try:
        auth_service = SQLAlchemyAuthService(db)
        return await auth_service.register_user(user_data)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    auth_service = SQLAlchemyAuthService(db)
    return await auth_service.authenticate_user(form_data.username, form_data.password)