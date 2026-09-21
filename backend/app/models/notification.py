"""
JobPilot AI — Notification & Automation Models
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON,
)
from sqlalchemy.orm import relationship
from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    type = Column(String(100), nullable=False)
    # new_matches | application_submitted | manual_action | assessment | interview | status_change | error | summary
    title = Column(String(500), nullable=False)
    message = Column(Text, nullable=True)
    data = Column(JSON, nullable=True)  # Additional context payload

    is_read = Column(Boolean, default=False)
    is_email_sent = Column(Boolean, default=False)
    is_push_sent = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    user = relationship("User", back_populates="notifications")


class EmailPreference(Base):
    __tablename__ = "email_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    new_matches = Column(Boolean, default=True)
    application_updates = Column(Boolean, default=True)
    manual_action_required = Column(Boolean, default=True)
    interview_updates = Column(Boolean, default=True)
    daily_summary = Column(Boolean, default=True)
    weekly_summary = Column(Boolean, default=True)
    marketing = Column(Boolean, default=False)

    email_provider = Column(String(50), default="default")  # gmail | outlook | smtp
    email_address = Column(String(255), nullable=True)  # Override email for notifications

    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    device_type = Column(String(50), nullable=True)  # android | ios | web
    device_token = Column(Text, nullable=True)  # Push notification token
    device_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)


class AutomationSession(Base):
    __tablename__ = "automation_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    status = Column(String(50), default="inactive")
    # inactive | active | paused | stopped | error
    mode = Column(String(50), default="manual")  # manual | review | auto

    # Daily counters
    jobs_scanned = Column(Integer, default=0)
    jobs_matched = Column(Integer, default=0)
    applications_prepared = Column(Integer, default=0)
    applications_submitted = Column(Integer, default=0)
    manual_review_required = Column(Integer, default=0)
    skipped = Column(Integer, default=0)
    errors = Column(Integer, default=0)

    # Limits
    daily_application_limit = Column(Integer, default=30)
    min_match_score_for_auto = Column(Float, default=85.0)

    # Per-portal pause
    paused_portals = Column(JSON, default=list)

    started_at = Column(DateTime(timezone=True), nullable=True)
    paused_at = Column(DateTime(timezone=True), nullable=True)
    stopped_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    user = relationship("User", back_populates="automation_sessions")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    session_id = Column(Integer, ForeignKey("automation_sessions.id", ondelete="SET NULL"), nullable=True)

    action = Column(String(255), nullable=False)
    resource_type = Column(String(100), nullable=True)
    resource_id = Column(Integer, nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
