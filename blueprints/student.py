from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.user import User
from models.internship import Internship
from models.applications import Application
from models.resume_score import ResumeScore
from models.saved_search import SavedSearch
from models.readiness_score import ReadinessScore
from models.saved_item import SavedItem
from models.recent_view import RecentView
from flask import render_template
from flask_login import login_required, current_user
from models.applications import Application
from ai.recommender import recommend_internships
import random
import json

from mcq_data import (
    accounting_mcqs, finance_mcqs, taxation_mcqs, auditing_mcqs, banking_mcqs,
    investment_research_mcqs, equity_research_mcqs, financial_modeling_mcqs,
    risk_management_mcqs, insurance_mcqs, wealth_management_mcqs,
    business_admin_mcqs, business_operations_mcqs, business_analytics_mcqs,
    logistics_mcqs, supply_chain_mcqs, hr_mcqs, marketing_mcqs,
    digital_marketing_mcqs, tools_mcqs, design_admin_mcqs,
    entrepreneurship_mcqs
)

student_bp = Blueprint("student", __name__, url_prefix="/student")

# =========================================================
# 🏠 STUDENT DASHBOARD
# =========================================================
@student_bp.route("/dashboard")
@login_required
def dashboard():

    readiness = ReadinessScore.get_score(current_user.id) or 0

    recent_apps = (
        Application.query
        .filter_by(user_id=current_user.id)
        .order_by(Application.created_at.desc())
        .limit(5)
        .all()
    )

    saved_count = SavedItem.query.filter_by(
        user_id=current_user.id,
        item_type="internship"
    ).count()

    recent_items = [
        rv.internship for rv in
        RecentView.query
        .filter_by(user_id=current_user.id)
        .order_by(RecentView.viewed_at.desc())
        .limit(5)
        .all()
    ]

    return render_template(
        "student/dashboard.html",
        student=current_user,
        readiness=readiness,
        applications=recent_apps,
        saved_count=saved_count,
        recommendations=recommend_internships(current_user)[:4],
        recent_items=recent_items
    )

# =========================================================
# 👤 PROFILE
# =========================================================
@student_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    if request.method == "POST":
        for field in ["name", "course", "skills", "tools", "location", "bio", "linkedin"]:
            setattr(current_user, field, request.form.get(field))
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("student.profile"))

    fields = [
        current_user.name, current_user.course, current_user.skills,
        current_user.tools, current_user.location,
        current_user.bio, current_user.linkedin
    ]
    completion = int((sum(bool(f) for f in fields) / len(fields)) * 100)

    return render_template(
        "student/profile.html",
        student=current_user,
        completion=completion
    )

# =========================================================
# 📄 RESUME SCORE
# =========================================================
@student_bp.route("/resume-score")
@login_required
def resume_score():

    obj = ResumeScore.query.filter_by(user_id=current_user.id).first()

    return render_template(
        "student/resume_score.html",
        resume_score=obj.score if obj else 0,
        suggestions=obj.suggestions if obj else []
    )

# =========================================================
# 📊 READINESS SCORE
# =========================================================
@student_bp.route("/score")
@login_required
def score():

    result = ReadinessScore.compute(current_user.id)

    return render_template(
        "student/readiness_score.html",
        score=result.get("total", 0),
        breakdown=result.get("breakdown", {}),
        suggestions=result.get("suggestions", [])
    )

# =========================================================
# 🔎 SAVED SEARCHES
# =========================================================
@student_bp.route("/saved-searches")
@login_required
def saved_searches():

    searches = SavedSearch.query.filter_by(user_id=current_user.id).all()
    return render_template("student/saved_searches.html", searches=searches)

# =========================================================
# ❤️ SAVE ITEM
# =========================================================
@student_bp.route("/save/<item_type>/<int:item_id>")
@login_required
def save_item(item_type, item_id):

    exists = SavedItem.query.filter_by(
        user_id=current_user.id,
        item_type=item_type,
        item_id=item_id
    ).first()

    if not exists:
        db.session.add(SavedItem(
            user_id=current_user.id,
            item_type=item_type,
            item_id=item_id
        ))
        db.session.commit()

    flash("Item saved successfully!", "success")
    return redirect(request.referrer or url_for("student.dashboard"))

# =========================================================
# ❤️ WISHLIST
# =========================================================
@student_bp.route("/wishlist")
@login_required
def wishlist():

    saved = SavedItem.query.filter_by(
        user_id=current_user.id,
        item_type="internship"
    ).all()

    internships = [Internship.query.get(i.item_id) for i in saved]

    return render_template(
        "student/wishlist.html",
        internships=internships
    )

# =========================================================
# 📁 APPLICATIONS
# =========================================================
@student_bp.route("/applications")
@login_required
def applications():

    apps = (
        Application.query
        .filter_by(user_id=current_user.id)
        .order_by(Application.created_at.desc())
        .all()
    )

    enriched = []
    for a in apps:
        internship = Internship.query.get(a.internship_id)
        enriched.append({
            "id": a.id,
            "status": a.status,
            "applied_at": a.created_at,
            "internship_title": internship.title if internship else "N/A",
            "company": internship.company_name if internship else "N/A",
            "location": internship.location if internship else "",
            "category": internship.category if internship else "",
        })

    return render_template("student/applications.html", applications=enriched)

# =========================================================
# ⭐ RECOMMENDATIONS
# =========================================================
@student_bp.route("/recommendations")
@login_required
def recommendations():

    return render_template(
        "student/recommendations.html",
        recommendations=recommend_internships(current_user)
    )

# =========================================================
# 🧠 MCQ TEST (SECURE)
# =========================================================
ALL_MCQS = {
    "Accounting": accounting_mcqs,
    "Finance": finance_mcqs,
    "Taxation": taxation_mcqs,
    "Auditing": auditing_mcqs,
    "Banking": banking_mcqs,
    "Investment Research": investment_research_mcqs,
    "Equity Research": equity_research_mcqs,
    "Financial Modeling": financial_modeling_mcqs,
    "Risk Management": risk_management_mcqs,
    "Insurance": insurance_mcqs,
    "Wealth Management": wealth_management_mcqs,
    "Business Administration": business_admin_mcqs,
    "Business Operations": business_operations_mcqs,
    "Business Analytics": business_analytics_mcqs,
    "Logistics": logistics_mcqs,
    "Supply Chain": supply_chain_mcqs,
    "HR": hr_mcqs,
    "Marketing": marketing_mcqs,
    "Digital Marketing": digital_marketing_mcqs,
    "Tools": tools_mcqs,
    "Design & Admin": design_admin_mcqs,
    "Entrepreneurship": entrepreneurship_mcqs
}

@student_bp.route("/mcq-test", methods=["GET", "POST"])
@login_required
def mcq_test():

    category = request.args.get("category", "")

    if request.method == "POST":
        questions = json.loads(request.form["questions"])
        score = 0
        results = []

        for i, q in enumerate(questions):
            user_ans = request.form.get(f"q{i}", "")
            score += int(user_ans == q["answer"])

            results.append({
                "question": q["question"],
                "options": [q["a"], q["b"], q["c"], q["d"]],
                "correct": q["answer"],
                "user": user_ans
            })

        return render_template(
            "student/mcq_result.html",
            results=results,
            score=score,
            total=len(questions),
            category=category
        )

    mcqs = ALL_MCQS.get(category, [])
    random_mcqs = random.sample(mcqs, min(10, len(mcqs)))

    return render_template(
        "student/mcq_test.html",
        mcqs=random_mcqs,
        category=category
    )


@student_bp.route("/applications")
@login_required
def my_applications():
    applications = (
        Application.query
        .filter_by(user_id=current_user.id)
        .order_by(Application.created_at.desc())
        .all()
    )

    return render_template(
        "student/my_applications.html",
        applications=applications
    )