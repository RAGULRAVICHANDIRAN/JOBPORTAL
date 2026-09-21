"""
JobPilot AI — Resume Model

Resume storage with versioning support.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON,
)
from sqlalchemy.orm import relationship
from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    name = Column(String(255), nullable=False)  # e.g. "Software Developer", "Data Analyst"
    file_path = Column(Text, nullable=True)
    file_type = Column(String(10), nullable=True)  # pdf | docx
    original_filename = Column(String(500), nullable=True)

    # Extracted content
    raw_text = Column(Text, nullable=True)
    parsed_data = Column(JSON, nullable=True)  # Structured extraction result

    # AI Analysis
    analysis_result = Column(JSON, nullable=True)  # Skills, strength, suggestions
    profile_strength = Column(Integer, default=0)  # 0-100

    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="resumes")
    versions = relationship("ResumeVersion", back_populates="resume", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Resume(id={self.id}, name='{self.name}')>"


class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)

    version_number = Column(Integer, nullable=False)
    file_path = Column(Text, nullable=True)
    raw_text = Column(Text, nullable=True)
    changes_description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    resume = relationship("Resume", back_populates="versions")

    def __repr__(self):
        return f"<ResumeVersion(resume_id={self.resume_id}, v={self.version_number})>"
