from models.internship import Internship
from models.user import User
from models.applications import Application
from app import db


def get_dashboard_metrics():

    # ------------------------------
    # BASIC COUNTS
    # ------------------------------
    total_internships = Internship.query.filter_by(status="Approved").count()
    total_students = User.query.filter_by(role="student").count()
    total_employers = User.query.filter_by(role="employer").count()

    # ------------------------------
    # CATEGORY-WISE INTERNSHIPS
    # ------------------------------
    category_data = (
        db.session.query(
            Internship.category,
            db.func.count(Internship.id)
        )
        .filter(Internship.status == "Approved")
        .group_by(Internship.category)
        .all()
    )

    # Convert to clean dict list
    categories = [
        {"category": cat or "Uncategorized", "count": count}
        for cat, count in category_data
    ]

    # ------------------------------
    # APPLICATION STATUS STATS
    # ------------------------------
    application_data = (
        db.session.query(
            Application.status,
            db.func.count(Application.id)
        )
        .group_by(Application.status)
        .all()
    )

    applications = [
        {"status": status or "Unknown", "count": count}
        for status, count in application_data
    ]

    # ------------------------------
    # TOP 5 LOCATIONS FOR INTERNSHIPS
    # ------------------------------
    location_data = (
        db.session.query(
            Internship.location,
            db.func.count(Internship.id)
        )
        .filter(Internship.status == "Approved")
        .group_by(Internship.location)
        .order_by(db.func.count(Internship.id).desc())
        .limit(5)
        .all()
    )

    locations = [
        {"location": loc or "Not Specified", "count": count}
        for loc, count in location_data
    ]

    # ------------------------------
    # TOP COMPANIES POSTING INTERNSHIPS
    # ------------------------------
    top_companies_data = (
        db.session.query(
            Internship.company,
            db.func.count(Internship.id)
        )
        .filter(Internship.status == "Approved")
        .group_by(Internship.company)
        .order_by(db.func.count(Internship.id).desc())
        .limit(5)
        .all()
    )

    top_companies = [
        {"company": comp or "Unknown", "count": count}
        for comp, count in top_companies_data
    ]

    # ------------------------------
    # STUDENT APPLICATION ACTIVITY
    # ------------------------------
    total_applications = Application.query.count()
    students_who_applied = (
        db.session.query(Application.user_id).distinct().count()
    )

    # ------------------------------
    # FINAL STRUCTURED OUTPUT
    # ------------------------------
    return {
        "totals": {
            "students": total_students,
            "employers": total_employers,
            "internships": total_internships,
            "applications": total_applications,
            "active_students": students_who_applied,
        },
        "categories": categories,
        "applications": applications,
        "top_locations": locations,
        "top_companies": top_companies,
    }