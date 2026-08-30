"""Alert database model."""

from enum import Enum
from typing import Optional

from sqlalchemy import String, Text, Enum as SQLEnum, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class AlertLevel(str, Enum):
    """Alert level enumeration."""
    
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class Alert(BaseModel):
    """Alert model representing system alerts."""
    
    __tablename__ = "alerts"
    
    # Basic information
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    level: Mapped[AlertLevel] = mapped_column(
        SQLEnum(AlertLevel),
        default=AlertLevel.INFO,
        nullable=False,
        index=True,
    )
    
    # Source
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    alert_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)
    acknowledged: Mapped[bool] = mapped_column(default=False, nullable=False)
    acknowledged_at: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Details
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Indices for performance
    __table_args__ = (
        Index("idx_alert_level_active", "level", "is_active"),
        Index("idx_alert_type_created", "alert_type", "created_at"),
        Index("idx_alert_acknowledged", "acknowledged"),
    )
    
    def __repr__(self) -> str:
        """String representation of alert."""
        return f"<Alert(id={self.id}, title={self.title}, level={self.level})>"
