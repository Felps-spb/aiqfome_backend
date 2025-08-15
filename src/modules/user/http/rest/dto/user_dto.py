from pydantic import BaseModel, EmailStr
import uuid

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserUpdateDTO(UserBase):
    pass 

class UserResponseDTO(UserBase):
    id: uuid.UUID

    class Config:
        orm_mode = True 