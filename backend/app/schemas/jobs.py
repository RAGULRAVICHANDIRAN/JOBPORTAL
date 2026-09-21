"""
JobPilot AI — Jobs Schemas

Pydantic models for job listing, filtering, detail, and match breakdown responses.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# --- Job Skill ---

class JobSkillResponse(BaseModel):
    id: int
    name: str
    is_required: bool = True
    category: Optional[str] = None
    model_config = {"from_attributes": True}


# --- Match Breakdown ---

class MatchBreakdown(BaseModel):
    overall_score: float = 0
    skills_score: float = 0
    experience_score: float = 0
    education_score: float = 0
    location_score: float = 0
    salary_score: float = 0
    preference_score: float = 0
    matching_skills: list[str] = []
    missing_skills: list[str] = []
    match_reasons: list[str] = []
    warnings: list[str] = []
    model_config = {"from_attributes": True}


# --- Job List Item ---

class JobListItem(BaseModel):
    id: int
    source: str
    title: str
    company: str
    location: Optional[str] = None
    remote_type: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: str = "INR"
    salary_period: str = "yearly"
    employment_type: Optional[str] = None
    experience_min: Optional[float] = None
    experience_max: Optional[float] = None
    company_type: Optional[str] = None
    posted_at: Optional[datetime] = None
    is_active: bool = True

    skills: list[JobSkillResponse] = []
    match_score: float = 0
    is_saved: bool = False

    model_config = {"from_attributes": True}


# --- Job Detail ---

class JobDetail(JobListItem):
    external_url: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    extracted_skills: list[str] = []
    extracted_keywords: list[str] = []
    deadline: Optional[datetime] = None
    created_at: datetime

    match: Optional[MatchBreakdown] = None


# --- Paginated Response ---

class PaginatedJobs(BaseModel):
    jobs: list[JobListItem]
    total: int
    page: int
    limit: int
    has_more: bool


# --- Save Job ---

class SavedJobResponse(BaseModel):
    message: str
    job_id: int
    is_saved: bool
