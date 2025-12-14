from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.skill_progress import SkillProgress

tests_bp = Blueprint("tests", __name__, url_prefix="/tests")

# -------------------------------------------------
# SKILL TESTS LANDING PAGE (CATEGORY SELECTION)
# -------------------------------------------------
@tests_bp.route("/skill-tests")
@login_required
def skill_tests():

    categories = [
        "Accounting", "Finance", "Taxation", "Auditing", "Banking",
        "Investment Research", "Equity Research", "Financial Modeling",
        "Risk Management", "Insurance", "Wealth Management",
        "Business Administration", "Business Operations",
        "Business Analytics", "Logistics", "Supply Chain",
        "HR", "Marketing", "Digital Marketing",
        "Tools", "Graphic Design", "Entrepreneurship"
    ]

    # 🔹 Fetch progress for logged-in user
    progress = SkillProgress.query.filter_by(
        user_id=current_user.id
    ).all()

    # Convert to dict for easy lookup in Jinja
    progress_map = {p.skill: p for p in progress}

    return render_template(
        "tests/skill_tests.html",
        categories=categories,
        progress_map=progress_map
    )