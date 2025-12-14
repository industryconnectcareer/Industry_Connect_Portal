from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from datetime import datetime
from extensions import db
from models.skill_progress import SkillProgress
from mcq_data import (
    accounting_mcqs, finance_mcqs, taxation_mcqs, auditing_mcqs,
    banking_mcqs, investment_research_mcqs, equity_research_mcqs,
    financial_modeling_mcqs, risk_management_mcqs, insurance_mcqs,
    wealth_management_mcqs, business_admin_mcqs, business_operations_mcqs,
    business_analytics_mcqs, logistics_mcqs, supply_chain_mcqs, hr_mcqs,
    marketing_mcqs, digital_marketing_mcqs, tools_mcqs, design_admin_mcqs,
    entrepreneurship_mcqs
)

resources_bp = Blueprint("resources", __name__, url_prefix="/resources")

PASS_MARKS = 60  # percentage


# -------------------------------------------------------
# MAIN RESOURCES LANDING PAGE
# -------------------------------------------------------
@resources_bp.route("/")
def index():
    return render_template("resources/index.html")


# -------------------------------------------------------
# RESUME TEMPLATES
# -------------------------------------------------------
@resources_bp.route("/resume-templates")
def resume_templates():
    return render_template("resources/resume_templates.html")


# -------------------------------------------------------
# EXCEL PRACTICE SHEETS
# -------------------------------------------------------
@resources_bp.route("/excel-practice")
def excel_practice():
    return render_template("resources/excel_practice.html")


# -------------------------------------------------------
# TALLY GUIDE
# -------------------------------------------------------
@resources_bp.route("/tally-guide")
def tally_guide():
    return render_template("resources/tally_guide.html")


# -------------------------------------------------------
# GST GUIDE
# -------------------------------------------------------
@resources_bp.route("/gst-guide")
def gst_guide():
    return render_template("resources/gst_guide.html")


# -------------------------------------------------------
# INTERVIEW QUESTIONS
# -------------------------------------------------------
@resources_bp.route("/interview-questions")
def interview_questions():
    return render_template("resources/interview_questions.html")


# -------------------------------------------------------
# MCQs (WITH SKILL PROGRESS)
# -------------------------------------------------------
@resources_bp.route("/mcqs_test", methods=["GET", "POST"])
@login_required
def mcqs_test():

    category = request.args.get("category")

    mcq_map = {
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
        "Graphic Design": design_admin_mcqs,
        "Entrepreneurship": entrepreneurship_mcqs
    }

    mcqs = mcq_map.get(category)

    if not mcqs:
        return "Invalid category", 404

    # --------- BLOCK REATTEMPT IF COMPLETED ---------
    progress = SkillProgress.query.filter_by(
        user_id=current_user.id,
        skill=category
    ).first()

    if progress and progress.status == "Completed":
        return redirect(url_for("tests.skill_tests"))

    # ---------- HANDLE TEST SUBMISSION ----------
    if request.method == "POST":

        correct = 0
        for i, q in enumerate(mcqs):
            if request.form.get(f"q{i}") == q["answer"]:
                correct += 1

        percentage = int((correct / len(mcqs)) * 100)

        if not progress:
            progress = SkillProgress(
                user_id=current_user.id,
                skill=category,
                attempts=0,
                best_score=0
            )
            db.session.add(progress)

        progress.attempts += 1
        progress.best_score = max(progress.best_score, percentage)
        progress.last_attempt = datetime.utcnow()
        progress.status = "Completed" if percentage >= PASS_MARKS else "Failed"

        db.session.commit()

        return render_template(
            "resources/mcq_result.html",
            category=category,
            score=percentage,
            status=progress.status
        )

    # ---------- SHOW THE TEST PAGE ----------
    return render_template(
        "resources/mcqs_test.html",
        category=category,
        mcqs=mcqs
    )


# -------------------------------------------------------
# APTITUDE PRACTICE
# -------------------------------------------------------
@resources_bp.route("/aptitude")
def aptitude():
    return render_template("resources/aptitude.html")


# -------------------------------------------------------
# CAREER ROADMAPS
# -------------------------------------------------------
@resources_bp.route("/career-roadmaps")
def career_roadmaps():
    return render_template("resources/career_roadmaps.html")


# -------------------------------------------------------
# SOFT SKILLS
# -------------------------------------------------------
@resources_bp.route("/soft-skills")
def soft_skills():
    return render_template("resources/soft_skills.html")


# -------------------------------------------------------
# AI TOOLS
# -------------------------------------------------------
@resources_bp.route("/ai-tools")
def ai_tools():
    return render_template("resources/ai_tools.html")


# -------------------------------------------------------
# DOWNLOAD CENTER
# -------------------------------------------------------
@resources_bp.route("/downloads")
def downloads():
    return render_template("resources/downloads.html")


# -------------------------------------------------------
# LINKEDIN GUIDE
# -------------------------------------------------------
@resources_bp.route("/linkedin-guide")
def linkedin_guide():
    return render_template("resources/linkedin_guide.html")


# -------------------------------------------------------
# PORTFOLIO GUIDE
# -------------------------------------------------------
@resources_bp.route("/portfolio-guide")
def portfolio_guide():
    return render_template("resources/portfolio_guide.html")
