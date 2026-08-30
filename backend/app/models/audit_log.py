"""AuditLog database model."""

from typing import Optional

from sqlalchemy import String, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class AuditLog(BaseModel):
    """AuditLog model for tracking changes."""
    
    __tablename__ = "audit_logs"
    
    # Action information
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_id: Mapped[int] = mapped_column(nullable=False, index=True)
    
    # User information
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Changes
    old_values: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    new_values: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Details
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Indices for performance
    __table_args__ = (
        Index("idx_audit_entity", "entity_type", "entity_id", "created_at"),
        Index("idx_audit_user", "user_id", "created_at"),
        Index("idx_audit_action", "action", "created_at"),
        Index("idx_audit_timestamp", "created_at"),
    )
    
    def __repr__(self) -> str:
        """String representation of audit log."""
        return f"<AuditLog(id={self.id}, action={self.action}, entity_type={self.entity_type}, entity_id={self.entity_id})>"
