"""Investigation database model."""

from enum import Enum
from typing import Optional

from sqlalchemy import String, Text, Enum as SQLEnum, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class InvestigationStatus(str, Enum):
    """Investigation status enumeration."""
    
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class InvestigationPhase(str, Enum):
    """Investigation phase enumeration."""
    
    INITIAL_ASSESSMENT = "initial_assessment"
    ROOT_CAUSE_ANALYSIS = "root_cause_analysis"
    REMEDIATION = "remediation"
    VERIFICATION = "verification"
    CLOSURE = "closure"


class Investigation(BaseModel):
    """Investigation model representing incident investigation."""
    
    __tablename__ = "investigations"
    
    # Basic information
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Status and phase
    status: Mapped[InvestigationStatus] = mapped_column(
        SQLEnum(InvestigationStatus),
        default=InvestigationStatus.PENDING,
        nullable=False,
        index=True,
    )
    phase: Mapped[InvestigationPhase] = mapped_column(
        SQLEnum(InvestigationPhase),
        default=InvestigationPhase.INITIAL_ASSESSMENT,
        nullable=False,
        index=True,
    )
    
    # Investigation details
    assigned_to: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    findings: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    root_cause: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommended_actions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timeline
    started_at: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    completed_at: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # AI Analysis
    ai_analysis: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_confidence: Mapped[Optional[float]] = mapped_column(nullable=True)
    ai_recommendations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Metadata
    tags: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Indices for performance
    __table_args__ = (
        Index("idx_investigation_status_created", "status", "created_at"),
        Index("idx_investigation_phase_created", "phase", "created_at"),
        Index("idx_investigation_assigned", "assigned_to"),
    )
    
    def __repr__(self) -> str:
        """String representation of investigation."""
        return f"<Investigation(id={self.id}, title={self.title}, status={self.status})>"
