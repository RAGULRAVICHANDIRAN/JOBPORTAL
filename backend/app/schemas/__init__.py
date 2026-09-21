"""JobPilot AI — Schemas Package"""

from app.schemas.auth import (
    RegisterRequest, LoginRequest, TokenResponse,
    RefreshRequest, UserResponse, MessageResponse,
)
from app.schemas.profile import (
    ProfileUpdate, ProfileResponse,
    SkillCreate, SkillResponse,
    EducationCreate, EducationResponse,
    ExperienceCreate, ExperienceResponse,
)
from app.schemas.jobs import (
    JobListItem, JobDetail, MatchBreakdown,
    PaginatedJobs, SavedJobResponse, JobSkillResponse,
)
