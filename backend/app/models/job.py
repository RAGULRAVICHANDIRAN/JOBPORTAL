"""
JobPilot AI — Job Models

Normalized job schema, job skills, match scores, filters, and application rules.
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


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(100), nullable=False, index=True)  # linkedin | indeed | mock
    external_job_id = Column(String(500), nullable=True)
    external_url = Column(Text, nullable=True)

    title = Column(String(500), nullable=False, index=True)
    company = Column(String(500), nullable=False, index=True)
    location = Column(String(500), nullable=True)
    remote_type = Column(String(50), nullable=True)  # remote | hybrid | onsite
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    salary_currency = Column(String(10), default="INR")
    salary_period = Column(String(20), default="yearly")  # yearly | monthly | hourly
    employment_type = Column(String(50), nullable=True)  # full-time | part-time | internship | contract
    experience_min = Column(Float, nullable=True)  # in years
    experience_max = Column(Float, nullable=True)
    company_type = Column(String(50), nullable=True)  # mnc | startup | product | service

    description = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    benefits = Column(Text, nullable=True)

    # AI-extracted data
    extracted_skills = Column(JSON, default=list)
    extracted_keywords = Column(JSON, default=list)

    posted_at = Column(DateTime(timezone=True), nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

    # Deduplication
    content_hash = Column(String(64), nullable=True, index=True)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    # Relationships
    skills = relationship("JobSkill", back_populates="job", cascade="all, delete-orphan")
    matches = relationship("JobMatch", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="job")

    __table_args__ = (
        UniqueConstraint("source", "external_job_id", name="uq_job_source_external"),
    )

    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', company='{self.company}')>"


class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)

    name = Column(String(255), nullable=False)
    is_required = Column(Boolean, default=True)
    category = Column(String(100), nullable=True)

    job = relationship("Job", back_populates="skills")

    def __repr__(self):
        return f"<JobSkill(name='{self.name}', required={self.is_required})>"


class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Overall
    overall_score = Column(Float, nullable=False, default=0)  # 0-100

    # Breakdown
    skills_score = Column(Float, default=0)
    experience_score = Column(Float, default=0)
    education_score = Column(Float, default=0)
    location_score = Column(Float, default=0)
    salary_score = Column(Float, default=0)
    preference_score = Column(Float, default=0)

    # AI Analysis
    matching_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)
    match_reasons = Column(JSON, default=list)
    warnings = Column(JSON, default=list)

    # Recommended resume
    recommended_resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    job = relationship("Job", back_populates="matches")

    __table_args__ = (
        UniqueConstraint("job_id", "user_id", name="uq_match_job_user"),
    )

    def __repr__(self):
        return f"<JobMatch(job_id={self.job_id}, score={self.overall_score})>"


class JobFilter(Base):
    __tablename__ = "job_filters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # Filter criteria
    job_titles = Column(JSON, default=list)
    locations = Column(JSON, default=list)
    remote_types = Column(JSON, default=list)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    experience_min = Column(Float, nullable=True)
    experience_max = Column(Float, nullable=True)
    employment_types = Column(JSON, default=list)
    company_types = Column(JSON, default=list)
    include_skills = Column(JSON, default=list)
    exclude_skills = Column(JSON, default=list)
    include_keywords = Column(JSON, default=list)
    exclude_keywords = Column(JSON, default=list)
    min_match_score = Column(Float, default=0)
    max_posting_age_days = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    user = relationship("User", back_populates="job_filters")

    def __repr__(self):
        return f"<JobFilter(name='{self.name}', active={self.is_active})>"


class ApplicationRule(Base):
    __tablename__ = "application_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)

    # Rule conditions (stored as structured JSON)
    conditions = Column(JSON, nullable=False)
    # Example: {"match_score_min": 80, "locations": ["Bangalore"], "experience": "fresher"}

    # Action
    action = Column(String(50), default="review")  # auto_apply | review | skip

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    def __repr__(self):
        return f"<ApplicationRule(name='{self.name}', action='{self.action}')>"
