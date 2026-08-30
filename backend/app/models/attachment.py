"""Attachment database model."""

from typing import Optional

from sqlalchemy import String, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Attachment(BaseModel):
    """Attachment model for file uploads."""
    
    __tablename__ = "attachments"
    
    # File information
    filename: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    
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
    comment_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("comments.id"),
        nullable=True,
        index=True,
    )
    uploaded_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    
    # Metadata
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_public: Mapped[bool] = mapped_column(default=False, nullable=False)
    download_count: Mapped[int] = mapped_column(default=0, nullable=False)
    
    # Indices for performance
    __table_args__ = (
        Index("idx_attachment_incident", "incident_id"),
        Index("idx_attachment_investigation", "investigation_id"),
        Index("idx_attachment_comment", "comment_id"),
        Index("idx_attachment_user", "uploaded_by", "created_at"),
    )
    
    def __repr__(self) -> str:
        """String representation of attachment."""
        return f"<Attachment(id={self.id}, filename={self.filename}, file_size={self.file_size})>"
