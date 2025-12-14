from app import db
from flask import Blueprint, render_template
from flask_login import login_required
from models.user import User
from models.internship import Internship
from models.applications import Application
from sqlalchemy import func, extract

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


# ====================================================
# ADMIN ANALYTICS DASHBOARD (UPGRADED)
# ====================================================
@analytics_bp.route("/")
@login_required
def analytics_dashboard():

    # ---------------------------------------
    # BASIC SYSTEM METRICS
    # ---------------------------------------
    total_students = User.query.filter_by(role="student").count()
    total_employers = User.query.filter_by(role="employer").count()
    total_internships = Internship.query.count()
    total_applications = Application.query.count()

    # ---------------------------------------
    # TOP INTERNSHIP CATEGORIES (SORTED)
    # ---------------------------------------
    category_stats = (
        db.session.query(
            Internship.category,
            func.count(Internship.id).label("count")
        )
        .group_by(Internship.category)
        .order_by(func.count(Internship.id).desc())
        .all()
    )

    # ---------------------------------------
    # TOP LOCATIONS (SORTED)
    # ---------------------------------------
    location_stats = (
        db.session.query(
            Internship.location,
            func.count(Internship.id).label("count")
        )
        .group_by(Internship.location)
        .order_by(func.count(Internship.id).desc())
        .all()
    )

    # ---------------------------------------
    # INTERNSHIP MODE DISTRIBUTION
    # ---------------------------------------
    mode_stats = (
        db.session.query(
            Internship.mode,
            func.count(Internship.id)
        )
        .group_by(Internship.mode)
        .all()
    )

    # ---------------------------------------
    # APPLICATION STATUS DISTRIBUTION
    # ---------------------------------------
    app_status_stats = (
        db.session.query(
            Application.status,
            func.count(Application.id)
        )
        .group_by(Application.status)
        .all()
    )

    # ---------------------------------------
    # MONTH-WISE APPLICATION TREND
    # ---------------------------------------
    monthly_applications = (
        db.session.query(
            extract('month', Application.created_at).label("month"),
            func.count(Application.id)
        )
        .group_by(extract('month', Application.created_at))
        .order_by("month")
        .all()
    )

    # ---------------------------------------
    # MONTH-WISE POSTINGS TREND
    # ---------------------------------------
    monthly_postings = (
        db.session.query(
            extract('month', Internship.created_at).label("month"),
            func.count(Internship.id)
        )
        .group_by(extract('month', Internship.created_at))
        .order_by("month")
        .all()
    )

    # ---------------------------------------
    # GROWTH STATS: STUDENTS & EMPLOYERS
    # ---------------------------------------
    student_growth = (
        db.session.query(
            extract('month', User.created_at).label("month"),
            func.count(User.id)
        )
        .filter(User.role == "student")
        .group_by(extract('month', User.created_at))
        .order_by("month")
        .all()
    )

    employer_growth = (
        db.session.query(
            extract('month', User.created_at).label("month"),
            func.count(User.id)
        )
        .filter(User.role == "employer")
        .group_by(extract('month', User.created_at))
        .order_by("month")
        .all()
    )

    # ---------------------------------------
    # CONVERSION FUNNEL DATA
    # ---------------------------------------
    applicants = total_applications
    shortlisted = Application.query.filter_by(status="Shortlisted").count()
    selected = Application.query.filter_by(status="Selected").count()

    funnel = {
        "applied": applicants,
        "shortlisted": shortlisted,
        "selected": selected,
    }

    # ---------------------------------------
    # SKILL DEMAND ANALYSIS (from internship 'skills' field)
    # ---------------------------------------
    raw_skills = (
        db.session.query(Internship.skills)
        .filter(Internship.skills.isnot(None))
        .all()
    )

    skill_count = {}

    for row in raw_skills:
        skill_list = [s.strip().lower() for s in row[0].split(",")]
        for skill in skill_list:
            if skill:
                skill_count[skill] = skill_count.get(skill, 0) + 1

    # Sort top 15 skills
    top_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)[:15]

    # ---------------------------------------
    # RETURN ANALYTICS TO TEMPLATE
    # ---------------------------------------
    return render_template(
        "admin/analytics.html",

        # Basic counters
        students=total_students,
        employers=total_employers,
        internships=total_internships,
        applications=total_applications,

        # Ranked analytics
        categories=category_stats,
        locations=location_stats,
        modes=mode_stats,
        app_trends=app_status_stats,

        # Trend graphs
        monthly_applications=monthly_applications,
        monthly_postings=monthly_postings,
        student_growth=student_growth,
        employer_growth=employer_growth,

        # Skills demand
        skills=top_skills,

        # Funnel analytics
        funnel=funnel
    )