from sqlalchemy import Column,ForeignKey,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.shared.database.psql import Base


class CartItemEntity(Base):
    __tablename__ = "cart_item"

    cart_id = Column(
        UUID(as_uuid=True),
        ForeignKey("carts.id", ondelete="CASCADE"),
        nullable=False
    )
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)

    cart = relationship("CartEntity", back_populates="items")
    product = relationship("ProductEntity")