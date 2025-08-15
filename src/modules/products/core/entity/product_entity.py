import uuid
from sqlalchemy import Column, String, Float, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.shared.database.psql import Base
from src.modules.carts.core.entity.carts_entity import cart_items_association 

class ProductEntity(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    image = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


