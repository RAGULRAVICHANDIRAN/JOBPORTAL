"""
JobPilot AI — Profile API Routes

CRUD for user profile, education, experience, and skills.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models.user import User
from app.models.profile import UserProfile, Education, Experience, Skill
from app.schemas.profile import (
    ProfileUpdate, ProfileResponse,
    SkillCreate, SkillResponse,
    EducationCreate, EducationResponse,
    ExperienceCreate, ExperienceResponse,
)
from app.core.deps import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])


async def _get_full_profile(db: AsyncSession, user_id: int) -> UserProfile:
    """Load profile with all relationships."""
    result = await db.execute(
        select(UserProfile)
        .where(UserProfile.user_id == user_id)
        .options(
            selectinload(UserProfile.education),
            selectinload(UserProfile.experience),
            selectinload(UserProfile.skills),
        )
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")
    return profile


def _calculate_profile_strength(profile: UserProfile) -> int:
    """Calculate profile completeness score (0-100)."""
    score = 0
    if profile.headline: score += 10
    if profile.summary: score += 10
    if profile.location: score += 5
    if profile.preferred_locations: score += 5
    if profile.work_authorization: score += 5
    if profile.preferred_job_titles: score += 5
    if profile.education and len(profile.education) > 0: score += 20
    if profile.experience and len(profile.experience) > 0: score += 20
    if profile.skills and len(profile.skills) >= 3: score += 15
    elif profile.skills and len(profile.skills) > 0: score += 5
    if profile.expected_salary_min: score += 5
    return min(score, 100)


@router.get("", response_model=ProfileResponse)
async def get_profile(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the current user's full profile."""
    profile = await _get_full_profile(db, user.id)
    return profile


@router.put("", response_model=ProfileResponse)
async def update_profile(
    data: ProfileUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update profile fields."""
    profile = await _get_full_profile(db, user.id)

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    profile.profile_strength = _calculate_profile_strength(profile)
    await db.flush()
    return await _get_full_profile(db, user.id)


# --- Education ---

@router.post("/education", response_model=EducationResponse, status_code=201)
async def add_education(
    data: EducationCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add an education entry."""
    profile = await _get_full_profile(db, user.id)
    edu = Education(profile_id=profile.id, **data.model_dump())
    db.add(edu)
    profile.profile_strength = _calculate_profile_strength(profile)
    await db.flush()
    return edu


@router.delete("/education/{edu_id}")
async def delete_education(
    edu_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete an education entry."""
    profile = await _get_full_profile(db, user.id)
    result = await db.execute(
        select(Education).where(Education.id == edu_id, Education.profile_id == profile.id)
    )
    edu = result.scalar_one_or_none()
    if not edu:
        raise HTTPException(status_code=404, detail="Education entry not found.")
    await db.delete(edu)
    return {"message": "Education deleted."}


# --- Experience ---

@router.post("/experience", response_model=ExperienceResponse, status_code=201)
async def add_experience(
    data: ExperienceCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add an experience entry."""
    profile = await _get_full_profile(db, user.id)
    exp = Experience(profile_id=profile.id, **data.model_dump())
    db.add(exp)
    profile.profile_strength = _calculate_profile_strength(profile)
    await db.flush()
    return exp


@router.delete("/experience/{exp_id}")
async def delete_experience(
    exp_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete an experience entry."""
    profile = await _get_full_profile(db, user.id)
    result = await db.execute(
        select(Experience).where(Experience.id == exp_id, Experience.profile_id == profile.id)
    )
    exp = result.scalar_one_or_none()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience entry not found.")
    await db.delete(exp)
    return {"message": "Experience deleted."}


# --- Skills ---

@router.post("/skills", response_model=SkillResponse, status_code=201)
async def add_skill(
    data: SkillCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add a skill."""
    profile = await _get_full_profile(db, user.id)
    skill = Skill(profile_id=profile.id, **data.model_dump())
    db.add(skill)
    profile.profile_strength = _calculate_profile_strength(profile)
    await db.flush()
    return skill


@router.delete("/skills/{skill_id}")
async def delete_skill(
    skill_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a skill."""
    profile = await _get_full_profile(db, user.id)
    result = await db.execute(
        select(Skill).where(Skill.id == skill_id, Skill.profile_id == profile.id)
    )
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found.")
    await db.delete(skill)
    return {"message": "Skill deleted."}
