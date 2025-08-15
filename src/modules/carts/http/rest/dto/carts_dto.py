import uuid
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


class ProductBaseDTO(BaseModel):
    title: str
    price: float
    description: Optional[str] = None
    category: Optional[str] = None
    image: str

class ProductActionDTO(BaseModel):
    product_id: uuid.UUID
    quantity: int = Field(1, gt=0) 

class CartCreateDTO(BaseModel):
    user_id: uuid.UUID = Field(alias='userId')
    products: List[ProductActionDTO]

class CartUpdateDTO(BaseModel):
    products: List[ProductActionDTO]

class CartItemResponseDTO(BaseModel):
    product: ProductBaseDTO
    quantity: int

    class Config:
        from_attributes = True
    
class CartResponseDTO(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    items: List[CartItemResponseDTO]

    class Config:
        from_attributes = True