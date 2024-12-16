from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from byocruda.core.database import Base

class TimestampMixin:
    """Mixin for timestamp columns"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

class Example(Base, TimestampMixin):
    """Example model to test database setup"""
    __tablename__ = "examples"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
