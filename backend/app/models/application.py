"""
JobPilot AI — Application Models

Application tracking, answers, cover letters, and immutable audit trail.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)

    # Status tracking
    status = Column(String(50), default="saved", nullable=False, index=True)
    # saved | ready | applied | assessment | interview | hr_round | offer | rejected | withdrawn | unknown

    # Application details
    portal_used = Column(String(100), nullable=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)
    cover_letter_id = Column(Integer, ForeignKey("cover_letters.id"), nullable=True)
    match_score = Column(Float, nullable=True)

    # Application method
    application_mode = Column(String(50), nullable=True)  # manual | review | auto
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    confirmation_received = Column(Boolean, default=False)
    external_application_id = Column(String(500), nullable=True)

    # Notes and tracking
    notes = Column(Text, nullable=True)
    interview_date = Column(DateTime(timezone=True), nullable=True)
    next_action = Column(Text, nullable=True)
    salary_offered = Column(Float, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    answers = relationship("ApplicationAnswer", back_populates="application", cascade="all, delete-orphan")
    cover_letter = relationship("CoverLetter", foreign_keys=[cover_letter_id])
    events = relationship("ApplicationEvent", back_populates="application", cascade="all, delete-orphan", order_by="ApplicationEvent.created_at")

    def __repr__(self):
        return f"<Application(id={self.id}, status='{self.status}')>"


class ApplicationAnswer(Base):
    __tablename__ = "application_answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    ai_suggested_answer = Column(Text, nullable=True)
    is_ai_generated = Column(Boolean, default=False)
    is_user_confirmed = Column(Boolean, default=False)
    is_sensitive = Column(Boolean, default=False)  # Requires manual answer
    is_reusable = Column(Boolean, default=False)  # User opted to save for reuse

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    application = relationship("Application", back_populates="answers")


class CoverLetter(Base):
    __tablename__ = "cover_letters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)

    content = Column(Text, nullable=False)
    is_ai_generated = Column(Boolean, default=False)
    is_edited = Column(Boolean, default=False)
    template_name = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)


class ApplicationEvent(Base):
    """Immutable audit trail for every application action."""
    __tablename__ = "application_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)

    event_type = Column(String(100), nullable=False)
    # discovered | matched | filtered | prepared | user_approved | submitted |
    # confirmation_received | status_changed | error | manual_action_required | skipped

    description = Column(Text, nullable=True)
    event_data = Column(JSON, nullable=True)
    status = Column(String(50), nullable=True)  # success | pending | failed | skipped

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    application = relationship("Application", back_populates="events")

    def __repr__(self):
        return f"<ApplicationEvent(type='{self.event_type}', status='{self.status}')>"
