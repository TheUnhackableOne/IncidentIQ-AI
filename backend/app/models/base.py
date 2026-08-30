"""SQLAlchemy ORM models base and utilities."""

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    
    pass


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps."""
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class IDMixin:
    """Mixin to add primary key id."""
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class BaseModel(Base, IDMixin, TimestampMixin):
    """Base model combining ID and timestamp mixins."""
    
    __abstract__ = True
