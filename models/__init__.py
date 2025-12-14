# models/__init__.py
"""
Centralized model loader for the entire application.

This makes it easier to import models across the project:
    from models import User, Internship, OJT
"""

# Core User + Company + College Models
from .user import User
from .company import Company
from .college import College

# Internship & OJT
from .internship import Internship
from .applications import Application
from .ojt import OJT

# Student Skill & AI Assessment Models
from .resume_score import ResumeScore
from .readiness_score import ReadinessScore
from .skill_progress import SkillProgress
from .skill_gap import SkillGap

# Search / Recommendations / Tracking
from .saved_search import SavedSearch
from .saved_item import SavedItem 
from .recent_view import RecentView

# Career Guidance Models
from .career_paths import CareerPath
from .interview_question import InterviewQuestion


# ----------------------------------------------------------
# OPTIONAL: Export list for IDEs & wildcard imports
# ----------------------------------------------------------
__all__ = [
    "User",
    "Company",
    "College",
    "Internship",
    "Application",
    "OJT",
    "ResumeScore",
    "ReadinessScore",
    "SkillBadge",
    "SkillGap",
    "SavedSearch",
    "SavedItem",
    "RecentView",
    "CareerPath",
    "InterviewQuestion",
]
