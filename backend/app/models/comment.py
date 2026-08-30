"""Comment database model."""

from typing import Optional

from sqlalchemy import String, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Comment(BaseModel):
    """Comment model for incident discussion."""
    
    __tablename__ = "comments"
    
    # Content
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Relationships
    incident_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=True,
        index=True,
    )
    investigation_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("investigations.id"),
        nullable=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    
    # Metadata
    author_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_edited: Mapped[bool] = mapped_column(default=False, nullable=False)
    edited_at: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Indices for performance
    __table_args__ = (
        Index("idx_comment_incident", "incident_id", "created_at"),
        Index("idx_comment_investigation", "investigation_id", "created_at"),
        Index("idx_comment_user", "user_id", "created_at"),
    )
    
    def __repr__(self) -> str:
        """String representation of comment."""
        return f"<Comment(id={self.id}, user_id={self.user_id}, incident_id={self.incident_id})>"
