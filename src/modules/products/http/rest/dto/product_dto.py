from pydantic import BaseModel
import uuid

class ProductCreateDTO(BaseModel):
    title: str
    price: float
    description: str
    category: str
    image: str

class ProductUpdateDTO(BaseModel):
    title: str | None = None
    price: float | None = None
    description: str | None = None
    category: str | None = None
    image: str | None = None

class ProductResponseDTO(BaseModel):
    id: uuid.UUID
    title: str
    price: float
    description: str
    category: str
    image: str

    class Config:
        orm_mode = True
