import uuid
from sqlalchemy import Column, ForeignKey, Integer, Table, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.shared.database.psql import Base

cart_items_association = Table(
    'cart_items', Base.metadata,
    Column('cart_id', UUID(as_uuid=True), ForeignKey('carts.id'), primary_key=True),
    Column('product_id', UUID(as_uuid=True), ForeignKey('products.id'), primary_key=True),
    Column('quantity', Integer, nullable=False, default=1)
)

class CartEntity(Base):
    __tablename__ = "carts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, unique=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("UserEntity", back_populates="cart")
    items = relationship("CartItemEntity", back_populates="cart", lazy="selectin")

    items = relationship(
        "CartItemEntity",
        back_populates="cart",
        cascade="all, delete-orphan",
        passive_deletes=True
    )