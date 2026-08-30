"""Incident database model."""

from enum import Enum
from typing import Optional

from sqlalchemy import String, Text, Enum as SQLEnum, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class IncidentStatus(str, Enum):
    """Incident status enumeration."""
    
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IncidentSeverity(str, Enum):
    """Incident severity enumeration."""
    
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Incident(BaseModel):
    """Incident model representing a reported incident."""
    
    __tablename__ = "incidents"
    
    # Basic information
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Status and severity
    status: Mapped[IncidentStatus] = mapped_column(
        SQLEnum(IncidentStatus),
        default=IncidentStatus.OPEN,
        nullable=False,
        index=True,
    )
    severity: Mapped[IncidentSeverity] = mapped_column(
        SQLEnum(IncidentSeverity),
        default=IncidentSeverity.MEDIUM,
        nullable=False,
        index=True,
    )
    
    # Timeline
    reported_at: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    started_at: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    resolved_at: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Investigation
    investigation_status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
    )
    investigation_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Metadata
    impact_area: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    affected_systems: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    root_cause: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    investigation_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("investigations.id"),
        nullable=True,
        index=True,
    )
    
    # Indices for performance
    __table_args__ = (
        Index("idx_incident_status_created", "status", "created_at"),
        Index("idx_incident_severity_created", "severity", "created_at"),
        Index("idx_incident_investigation", "investigation_id"),
    )
    
    def __repr__(self) -> str:
        """String representation of incident."""
        return f"<Incident(id={self.id}, title={self.title}, status={self.status})>"
