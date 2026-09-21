"""
JobPilot AI — Profile Schemas

Pydantic models for profile, education, experience, and skill CRUD.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# --- Skill ---

class SkillCreate(BaseModel):
    name: str = Field(..., max_length=255)
    category: Optional[str] = None
    proficiency: int = Field(default=50, ge=0, le=100)
    years_of_experience: float = 0
    is_primary: bool = False


class SkillResponse(SkillCreate):
    id: int
    model_config = {"from_attributes": True}


# --- Education ---

class EducationCreate(BaseModel):
    degree: str = Field(..., max_length=255)
    field_of_study: Optional[str] = None
    university: str = Field(..., max_length=500)
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = Field(default=None, ge=0, le=10)
    percentage: Optional[float] = Field(default=None, ge=0, le=100)
    is_current: bool = False


class EducationResponse(EducationCreate):
    id: int
    model_config = {"from_attributes": True}


# --- Experience ---

class ExperienceCreate(BaseModel):
    type: str = Field(..., pattern="^(work|internship|project|freelance)$")
    title: str = Field(..., max_length=255)
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: bool = False
    technologies: list[str] = []


class ExperienceResponse(ExperienceCreate):
    id: int
    model_config = {"from_attributes": True}


# --- Profile ---

class ProfileUpdate(BaseModel):
    headline: Optional[str] = None
    summary: Optional[str] = None
    location: Optional[str] = None
    preferred_locations: Optional[list[str]] = None
    work_authorization: Optional[str] = None
    preferred_job_titles: Optional[list[str]] = None
    preferred_employment_types: Optional[list[str]] = None
    expected_salary_min: Optional[float] = None
    expected_salary_max: Optional[float] = None
    salary_currency: Optional[str] = "INR"
    willing_to_relocate: Optional[bool] = None


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    headline: Optional[str] = None
    summary: Optional[str] = None
    location: Optional[str] = None
    preferred_locations: list[str] = []
    work_authorization: Optional[str] = None
    preferred_job_titles: list[str] = []
    preferred_employment_types: list[str] = []
    expected_salary_min: Optional[float] = None
    expected_salary_max: Optional[float] = None
    salary_currency: str = "INR"
    willing_to_relocate: bool = False
    profile_strength: int = 0

    education: list[EducationResponse] = []
    experience: list[ExperienceResponse] = []
    skills: list[SkillResponse] = []

    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
