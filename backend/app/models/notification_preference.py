"""NotificationPreference database model."""

from typing import Optional

from sqlalchemy import String, Boolean, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class NotificationPreference(BaseModel):
    """NotificationPreference model for user notification settings."""
    
    __tablename__ = "notification_preferences"
    
    # User relationship
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    
    # Email notifications
    email_on_incident_created: Mapped[bool] = mapped_column(default=True, nullable=False)
    email_on_incident_updated: Mapped[bool] = mapped_column(default=True, nullable=False)
    email_on_incident_closed: Mapped[bool] = mapped_column(default=True, nullable=False)
    email_on_investigation_started: Mapped[bool] = mapped_column(default=True, nullable=False)
    email_on_investigation_completed: Mapped[bool] = mapped_column(default=True, nullable=False)
    email_on_comment_added: Mapped[bool] = mapped_column(default=False, nullable=False)
    email_on_alert: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    # Notification frequency
    notification_frequency: Mapped[str] = mapped_column(
        String(50),
        default="immediate",
        nullable=False,
    )  # immediate, daily, weekly
    
    # Push notifications
    push_notifications_enabled: Mapped[bool] = mapped_column(default=True, nullable=False)
    push_on_critical_alert: Mapped[bool] = mapped_column(default=True, nullable=False)
    push_on_assigned_incident: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    # SMS notifications
    sms_notifications_enabled: Mapped[bool] = mapped_column(default=False, nullable=False)
    sms_phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    sms_on_critical_alert: Mapped[bool] = mapped_column(default=False, nullable=False)
    
    # In-app notifications
    in_app_notifications_enabled: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    # Do not disturb
    do_not_disturb_enabled: Mapped[bool] = mapped_column(default=False, nullable=False)
    do_not_disturb_start: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)  # HH:MM
    do_not_disturb_end: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)    # HH:MM
    
    # Indices for performance
    __table_args__ = (
        Index("idx_notification_pref_user", "user_id"),
    )
    
    def __repr__(self) -> str:
        """String representation of notification preference."""
        return f"<NotificationPreference(id={self.id}, user_id={self.user_id})>"
