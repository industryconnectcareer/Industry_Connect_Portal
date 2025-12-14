from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ai.career_predictor import predict_role
from ai.skill_gap_ai import analyze_skill_gap
from models.career_paths import CareerPath

career_bp = Blueprint("career", __name__, url_prefix="/career")

# --------------------------------
# CAREER NAVIGATOR HOME
# --------------------------------
@career_bp.route("/path")
@login_required
def career_path():
    """
    Shows all commerce-related career paths (CA, CS, CFA, Banking, HR, etc.)
    pulled dynamically from database.
    """
    paths = CareerPath.query.order_by(CareerPath.category.asc()).all()
    return render_template("career/career_path.html", paths=paths)


# --------------------------------
# RECOMMENDED ROLES (AI)
# --------------------------------
@career_bp.route("/recommended")
@login_required
def recommended_roles():
    """
    Predicts best-fit commerce career roles based on student's skill profile.
    Uses:
        - expanded skill-to-role mapping
        - skill-gap analysis
    """
    # Handle missing skill data safely
    student_skills = []
    if current_user.skills:
        student_skills = [s.strip() for s in current_user.skills.split(",") if s.strip()]

    # AI predictions
    top_roles = predict_role(student_skills)
    gaps = analyze_skill_gap(student_skills)

    return render_template(
        "career/recommended_roles.html",
        roles=top_roles,
        gaps=gaps,
        student_skills=student_skills
    )


# --------------------------------
# COMMERCE STREAMS INFORMATION PAGE
# --------------------------------
@career_bp.route("/streams")
def commerce_streams():
    """
    Displays detailed information about:
    - CA / CS / CMA
    - Banking & Finance
    - Management careers
    - Marketing & Digital Marketing
    - Taxation
    - Law (LLB)
    - Entrepreneurship
    - E-Commerce
    - CPA, ACCA, CFA
    - Actuarial Science
    """
    return render_template("career/commerce_streams.html")


# --------------------------------
# DETAILED CAREER PAGE
# (optional upgrade for CA, CS, CMA, Banking, Marketing, etc.)
# --------------------------------
@career_bp.route("/career/<slug>")
def view_career(slug):
    """
    Allows each career to have its own SEO-friendly page:
        /career/chartered-accountant
        /career/investment-banking
        /career/hr-manager
        /career/financial-analyst
    """
    path = CareerPath.query.filter_by(slug=slug).first_or_404()
    return render_template("career/career_detail.html", path=path)