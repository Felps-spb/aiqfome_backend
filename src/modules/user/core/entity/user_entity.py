from sqlalchemy import Column, String, UUID, DateTime, func
from sqlalchemy.orm import relationship
from src.shared.database.psql import Base

class UserEntity(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    cart = relationship("CartEntity", back_populates="user", uselist=False)
