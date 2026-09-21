"""
JobPilot AI — Models Package

Imports all models so SQLAlchemy can discover them for table creation.
"""

from app.models.user import User
from app.models.profile import UserProfile, Education, Experience, Skill
from app.models.resume import Resume, ResumeVersion
from app.models.job import Job, JobSkill, JobMatch, JobFilter, ApplicationRule
from app.models.portal import JobPortal, ConnectedAccount
from app.models.application import Application, ApplicationAnswer, CoverLetter, ApplicationEvent
from app.models.notification import Notification, EmailPreference, Device, AutomationSession, AuditLog

__all__ = [
    "User",
    "UserProfile", "Education", "Experience", "Skill",
    "Resume", "ResumeVersion",
    "Job", "JobSkill", "JobMatch", "JobFilter", "ApplicationRule",
    "JobPortal", "ConnectedAccount",
    "Application", "ApplicationAnswer", "CoverLetter", "ApplicationEvent",
    "Notification", "EmailPreference", "Device", "AutomationSession", "AuditLog",
]
