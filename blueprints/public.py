from flask import Blueprint, render_template, request
from models.internship import Internship
from models.ojt import OJT
from models.user import User
from ai.recommender import recommend_internships  # OPTIONAL (if enabled)

public_bp = Blueprint("public", __name__)


# =====================================================
# HOME PAGE
# =====================================================
@public_bp.route("/")
def home():

    # ---------- Stats ----------
    stats = {
        "internships": Internship.query.filter_by(status="Approved").count(),
        "ojts": OJT.query.filter_by(status="Approved").count(),
        "companies": User.query.filter_by(role="employer").count(),
        "students": User.query.filter_by(role="student").count(),
    }

    # ---------- Latest ----------
    latest_internships = (
        Internship.query.filter_by(status="Approved")
        .order_by(Internship.id.desc())
        .limit(4)
        .all()
    )

    latest_ojts = (
        OJT.query.filter_by(status="Approved")
        .order_by(OJT.id.desc())
        .limit(4)
        .all()
    )

    # ---------- Trending ----------
    trending_internships = (
        Internship.query.filter_by(status="Approved")
        .order_by(Internship.views.desc())
        .limit(5)
        .all()
        if hasattr(Internship, "views") else []
    )

    trending_ojts = (
        OJT.query.filter_by(status="Approved")
        .order_by(OJT.enrolled_count.desc())
        .limit(5)
        .all()
        if hasattr(OJT, "enrolled_count") else []
    )

    # ---------- AI Recommendations ----------
    recommended = []
    try:
        from flask_login import current_user
        if current_user.is_authenticated and hasattr(current_user, "skills"):
            recommended = recommend_internships(current_user.skills)
    except:
        recommended = []

    return render_template(
        "home.html",
        stats=stats,
        latest_internships=latest_internships,
        latest_ojts=latest_ojts,
        trending_internships=trending_internships,
        trending_ojts=trending_ojts,
        recommended=recommended
    )


# =====================================================
# CATEGORY BROWSER
# =====================================================
@public_bp.route("/categories")
def categories():

    category_list = [
        {"id": "accounting",     "name": "Accounting",        "icon": "📘"},
        {"id": "finance",        "name": "Finance",           "icon": "📊"},
        {"id": "taxation",       "name": "Taxation",          "icon": "🧾"},
        {"id": "banking",        "name": "Banking",           "icon": "🏦"},
        {"id": "hr",             "name": "Human Resources",   "icon": "👥"},
        {"id": "marketing",      "name": "Marketing",         "icon": "📣"},
        {"id": "analytics",      "name": "Business Analytics","icon": "📈"},
        {"id": "supplychain",    "name": "Supply Chain",      "icon": "🚚"},
    ]

    # Add internship + OJT count to each category
    for cat in category_list:
        cat["internship_count"] = Internship.query.filter_by(
            category=cat["id"], status="Approved"
        ).count()

        cat["ojt_count"] = OJT.query.filter_by(
            category=cat["id"], status="Approved"
        ).count()

    return render_template(
        "internships/categories.html",
        categories=category_list
    )


# =====================================================
# UNIVERSAL SEARCH → Internships + OJT
# =====================================================
@public_bp.route("/search")
def search():

    query = request.args.get("q", "").strip()

    if not query:
        return render_template(
            "search/search_results.html",
            query=query,
            internships=[],
            ojts=[]
        )

    # ---------- Internship Search ----------
    internships = Internship.query.filter(
        (Internship.title.ilike(f"%{query}%")) |
        (Internship.skills.ilike(f"%{query}%")) |
        (Internship.category.ilike(f"%{query}%")) |
        (Internship.company_name.ilike(f"%{query}%")) |
        (Internship.location.ilike(f"%{query}%")) |
        (Internship.description.ilike(f"%{query}%"))
    ).filter_by(status="Approved").all()

    # ---------- OJT Search ----------
    ojts = OJT.query.filter(
        (OJT.title.ilike(f"%{query}%")) |
        (OJT.description.ilike(f"%{query}%")) |
        (OJT.category.ilike(f"%{query}%"))
    ).filter_by(status="Approved").all()

    return render_template(
        "search/search_results.html",
        query=query,
        internships=internships,
        ojts=ojts
    )