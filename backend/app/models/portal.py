"""
JobPilot AI — Portal Models

Job portal connectors and connected account tracking.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class JobPortal(Base):
    __tablename__ = "job_portals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)  # linkedin, indeed, naukri
    icon_url = Column(Text, nullable=True)
    base_url = Column(Text, nullable=True)

    # Capabilities
    supports_search = Column(Boolean, default=False)
    supports_apply = Column(Boolean, default=False)
    supports_status_tracking = Column(Boolean, default=False)
    supports_oauth = Column(Boolean, default=False)
    requires_manual_auth = Column(Boolean, default=True)

    is_active = Column(Boolean, default=True)
    is_demo = Column(Boolean, default=False)  # True for mock/demo portals

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    connected_accounts = relationship("ConnectedAccount", back_populates="portal")

    def __repr__(self):
        return f"<JobPortal(name='{self.name}', slug='{self.slug}')>"


class ConnectedAccount(Base):
    __tablename__ = "connected_accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    portal_id = Column(Integer, ForeignKey("job_portals.id", ondelete="CASCADE"), nullable=False)

    # Connection status
    is_connected = Column(Boolean, default=False)
    connection_status = Column(String(50), default="disconnected")  # connected | disconnected | expired | error

    # Secure token storage (encrypted in production)
    access_token_encrypted = Column(Text, nullable=True)
    refresh_token_encrypted = Column(Text, nullable=True)
    token_expires_at = Column(DateTime(timezone=True), nullable=True)

    # Sync info
    last_synced_at = Column(DateTime(timezone=True), nullable=True)
    sync_error = Column(Text, nullable=True)

    # Portal-specific profile data
    portal_username = Column(String(255), nullable=True)
    portal_profile_url = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    user = relationship("User", back_populates="connected_accounts")
    portal = relationship("JobPortal", back_populates="connected_accounts")

    __table_args__ = (
        UniqueConstraint("user_id", "portal_id", name="uq_user_portal"),
    )

    def __repr__(self):
        return f"<ConnectedAccount(user_id={self.user_id}, portal_id={self.portal_id})>"
