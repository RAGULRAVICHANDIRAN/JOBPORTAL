"""
JobPilot AI — Jobs API Routes

Browse, search, filter, and save jobs. Includes on-the-fly match scoring
based on the user's profile skills (simple set-intersection algorithm).
"""

import math
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc, asc
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models.user import User
from app.models.job import Job, JobSkill, JobMatch
from app.models.profile import UserProfile, Skill
from app.models.application import Application
from app.schemas.jobs import (
    JobListItem, JobDetail, MatchBreakdown,
    PaginatedJobs, SavedJobResponse,
)
from app.core.deps import get_current_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

async def _compute_match_score(
    db: AsyncSession, user_id: int, job: Job,
) -> MatchBreakdown:
    """
    Simple profile-vs-job match scoring using skill overlap.
    No AI needed — just set intersection math.
    """
    # Load user skills
    profile_result = await db.execute(
        select(UserProfile)
        .where(UserProfile.user_id == user_id)
        .options(selectinload(UserProfile.skills))
    )
    profile = profile_result.scalar_one_or_none()

    if not profile or not profile.skills:
        return MatchBreakdown(
            overall_score=0,
            warnings=["Complete your profile to see match scores."],
        )

    user_skills = {s.name.lower().strip() for s in profile.skills}
    job_skills_required = {s.name.lower().strip() for s in job.skills if s.is_required}
    job_skills_nice = {s.name.lower().strip() for s in job.skills if not s.is_required}
    all_job_skills = job_skills_required | job_skills_nice

    matching = user_skills & all_job_skills
    missing = job_skills_required - user_skills

    # Skills score (60% weight) — required skills matter more
    if job_skills_required:
        required_match = len(user_skills & job_skills_required) / len(job_skills_required)
    else:
        required_match = 1.0

    if job_skills_nice:
        nice_match = len(user_skills & job_skills_nice) / len(job_skills_nice)
    else:
        nice_match = 1.0

    skills_score = round((required_match * 0.8 + nice_match * 0.2) * 100, 1)

    # Experience score (20% weight) — check if user experience range fits
    experience_score = 70.0  # Default reasonable score
    if profile.experience:
        total_exp_years = len(profile.experience) * 0.5  # rough estimate
        if job.experience_max is not None and total_exp_years <= job.experience_max:
            experience_score = 90.0
        if job.experience_min is not None and total_exp_years < job.experience_min:
            experience_score = 40.0

    # Location score (10% weight)
    location_score = 60.0
    if job.remote_type == "remote":
        location_score = 100.0
    elif profile.preferred_locations:
        pref_locs = [loc.lower() for loc in profile.preferred_locations]
        if job.location and job.location.lower() in pref_locs:
            location_score = 100.0

    # Salary score (10% weight)
    salary_score = 70.0
    if profile.expected_salary_min and job.salary_max:
        if job.salary_max >= profile.expected_salary_min:
            salary_score = 90.0
        else:
            salary_score = 40.0

    # Overall
    overall = round(
        skills_score * 0.6
        + experience_score * 0.2
        + location_score * 0.1
        + salary_score * 0.1,
        1,
    )

    # Build reasons
    reasons = []
    if matching:
        reasons.append(f"You have {len(matching)} matching skill(s)")
    if job.remote_type == "remote":
        reasons.append("This is a remote position")
    if job.experience_min is not None and job.experience_min == 0:
        reasons.append("Open to freshers")

    warnings = []
    if missing:
        warnings.append(f"Missing required skill(s): {', '.join(s.title() for s in missing)}")

    return MatchBreakdown(
        overall_score=overall,
        skills_score=skills_score,
        experience_score=experience_score,
        education_score=70.0,  # Placeholder
        location_score=location_score,
        salary_score=salary_score,
        preference_score=overall,
        matching_skills=[s.title() for s in matching],
        missing_skills=[s.title() for s in missing],
        match_reasons=reasons,
        warnings=warnings,
    )


async def _get_saved_job_ids(db: AsyncSession, user_id: int) -> set[int]:
    """Get set of job IDs that the user has saved."""
    result = await db.execute(
        select(Application.job_id)
        .where(Application.user_id == user_id, Application.status == "saved")
    )
    return {row[0] for row in result.all() if row[0] is not None}


# ──────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────

@router.get("", response_model=PaginatedJobs)
async def list_jobs(
    search: str = Query(default="", description="Search by title or company"),
    remote_type: str = Query(default="", description="Filter: remote | hybrid | onsite"),
    employment_type: str = Query(default="", description="Filter: full-time | internship | contract | part-time"),
    experience_max: float | None = Query(default=None, description="Max experience in years"),
    salary_min: float | None = Query(default=None, description="Min salary"),
    company_type: str = Query(default="", description="Filter: mnc | startup | product | service"),
    sort_by: str = Query(default="posted_at", description="Sort: posted_at | salary | match"),
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=20, ge=1, le=50, description="Items per page"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List jobs with filtering, sorting, and pagination."""
    query = select(Job).where(Job.is_active == True).options(  # noqa: E712
        selectinload(Job.skills)
    )

    # --- Filters ---
    if search:
        search_term = f"%{search.strip()}%"
        query = query.where(
            or_(
                Job.title.ilike(search_term),
                Job.company.ilike(search_term),
                Job.location.ilike(search_term),
            )
        )

    if remote_type:
        query = query.where(Job.remote_type == remote_type.lower())

    if employment_type:
        query = query.where(Job.employment_type == employment_type.lower())

    if experience_max is not None:
        query = query.where(
            or_(Job.experience_min == None, Job.experience_min <= experience_max)  # noqa: E711
        )

    if salary_min is not None:
        query = query.where(
            or_(Job.salary_max == None, Job.salary_max >= salary_min)  # noqa: E711
        )

    if company_type:
        query = query.where(Job.company_type == company_type.lower())

    # --- Count total ---
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # --- Sorting ---
    if sort_by == "salary":
        query = query.order_by(desc(Job.salary_max).nulls_last())
    else:
        query = query.order_by(desc(Job.posted_at).nulls_last())

    # --- Pagination ---
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    jobs = result.scalars().unique().all()

    # Compute match scores and saved status
    saved_ids = await _get_saved_job_ids(db, user.id)

    job_items = []
    for job in jobs:
        match = await _compute_match_score(db, user.id, job)
        item = JobListItem(
            id=job.id,
            source=job.source,
            title=job.title,
            company=job.company,
            location=job.location,
            remote_type=job.remote_type,
            salary_min=job.salary_min,
            salary_max=job.salary_max,
            salary_currency=job.salary_currency,
            salary_period=job.salary_period,
            employment_type=job.employment_type,
            experience_min=job.experience_min,
            experience_max=job.experience_max,
            company_type=job.company_type,
            posted_at=job.posted_at,
            is_active=job.is_active,
            skills=[s for s in job.skills],
            match_score=match.overall_score,
            is_saved=job.id in saved_ids,
        )
        job_items.append(item)

    # Sort by match score if requested (post-compute)
    if sort_by == "match":
        job_items.sort(key=lambda j: j.match_score, reverse=True)

    has_more = (page * limit) < total

    return PaginatedJobs(
        jobs=job_items,
        total=total,
        page=page,
        limit=limit,
        has_more=has_more,
    )


@router.get("/{job_id}", response_model=JobDetail)
async def get_job_detail(
    job_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get full job detail with match score breakdown."""
    result = await db.execute(
        select(Job)
        .where(Job.id == job_id)
        .options(selectinload(Job.skills))
    )
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found.",
        )

    match = await _compute_match_score(db, user.id, job)
    saved_ids = await _get_saved_job_ids(db, user.id)

    return JobDetail(
        id=job.id,
        source=job.source,
        title=job.title,
        company=job.company,
        location=job.location,
        remote_type=job.remote_type,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        salary_currency=job.salary_currency,
        salary_period=job.salary_period,
        employment_type=job.employment_type,
        experience_min=job.experience_min,
        experience_max=job.experience_max,
        company_type=job.company_type,
        posted_at=job.posted_at,
        is_active=job.is_active,
        external_url=job.external_url,
        description=job.description,
        requirements=job.requirements,
        benefits=job.benefits,
        extracted_skills=job.extracted_skills or [],
        extracted_keywords=job.extracted_keywords or [],
        deadline=job.deadline,
        created_at=job.created_at,
        skills=[s for s in job.skills],
        match_score=match.overall_score,
        is_saved=job.id in saved_ids,
        match=match,
    )


@router.post("/{job_id}/save", response_model=SavedJobResponse)
async def save_job(
    job_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Save/bookmark a job."""
    # Check job exists
    job_result = await db.execute(select(Job).where(Job.id == job_id))
    if not job_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Job not found.")

    # Check if already saved
    existing = await db.execute(
        select(Application).where(
            Application.user_id == user.id,
            Application.job_id == job_id,
            Application.status == "saved",
        )
    )
    if existing.scalar_one_or_none():
        return SavedJobResponse(message="Job already saved.", job_id=job_id, is_saved=True)

    # Create saved application
    app = Application(
        user_id=user.id,
        job_id=job_id,
        status="saved",
        application_mode="manual",
    )
    db.add(app)
    await db.flush()

    return SavedJobResponse(message="Job saved successfully.", job_id=job_id, is_saved=True)


@router.delete("/{job_id}/save", response_model=SavedJobResponse)
async def unsave_job(
    job_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Remove a saved/bookmarked job."""
    result = await db.execute(
        select(Application).where(
            Application.user_id == user.id,
            Application.job_id == job_id,
            Application.status == "saved",
        )
    )
    app = result.scalar_one_or_none()

    if not app:
        return SavedJobResponse(message="Job was not saved.", job_id=job_id, is_saved=False)

    await db.delete(app)
    await db.flush()

    return SavedJobResponse(message="Job removed from saved.", job_id=job_id, is_saved=False)
