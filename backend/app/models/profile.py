"""
JobPilot AI — Profile Models

UserProfile, Education, Experience, Skill — comprehensive professional profile.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON,
)
from sqlalchemy.orm import relationship
from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Personal
    headline = Column(String(500), nullable=True)
    summary = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    preferred_locations = Column(JSON, default=list)  # ["Bangalore", "Chennai", "Remote"]
    work_authorization = Column(String(100), nullable=True)  # e.g. "Indian Citizen", "H1B"

    # Preferences
    preferred_job_titles = Column(JSON, default=list)
    preferred_employment_types = Column(JSON, default=list)  # ["Full-time", "Internship"]
    expected_salary_min = Column(Float, nullable=True)
    expected_salary_max = Column(Float, nullable=True)
    salary_currency = Column(String(10), default="INR")
    willing_to_relocate = Column(Boolean, default=False)

    # Profile completeness
    profile_strength = Column(Integer, default=0)  # 0-100

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="profile")
    education = relationship("Education", back_populates="profile", cascade="all, delete-orphan", order_by="Education.graduation_year.desc()")
    experience = relationship("Experience", back_populates="profile", cascade="all, delete-orphan", order_by="Experience.start_date.desc()")
    skills = relationship("Skill", back_populates="profile", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id})>"


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False)

    degree = Column(String(255), nullable=False)  # e.g. "B.Tech", "M.Sc"
    field_of_study = Column(String(255), nullable=True)  # e.g. "Computer Science"
    university = Column(String(500), nullable=False)
    graduation_year = Column(Integer, nullable=True)
    cgpa = Column(Float, nullable=True)
    percentage = Column(Float, nullable=True)
    is_current = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    profile = relationship("UserProfile", back_populates="education")

    def __repr__(self):
        return f"<Education(degree='{self.degree}', university='{self.university}')>"


class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False)

    type = Column(String(50), nullable=False)  # work | internship | project | freelance
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    is_current = Column(Boolean, default=False)
    technologies = Column(JSON, default=list)  # ["Python", "Django", "PostgreSQL"]

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    profile = relationship("UserProfile", back_populates="experience")

    def __repr__(self):
        return f"<Experience(title='{self.title}', company='{self.company}')>"


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False)

    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True)  # programming | framework | database | cloud | soft_skill
    proficiency = Column(Integer, default=50)  # 0-100
    years_of_experience = Column(Float, default=0)
    is_primary = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    profile = relationship("UserProfile", back_populates="skills")

    def __repr__(self):
        return f"<Skill(name='{self.name}', proficiency={self.proficiency})>"
