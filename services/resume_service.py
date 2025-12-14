import re
import json
from models.resume_score import ResumeScore
from app import db


# ---------------------------------------------------------
# MASTER KEYWORD BANK – Commerce + Finance + Accounting
# ---------------------------------------------------------
KEYWORD_GROUPS = {
    "technical": [
        "excel", "advanced excel", "tally", "gst", "accounting",
        "financial analysis", "data analysis", "pivot table",
        "vlookup", "mis reporting", "sql", "power bi",
        "financial modelling", "taxation", "budgeting"
    ],
    "finance": [
        "balance sheet", "profit and loss", "cash flow", "audit",
        "investment", "equity", "mutual fund", "share market"
    ],
    "soft_skills": [
        "communication", "leadership", "critical thinking",
        "problem solving", "teamwork", "analytical skills"
    ]
}

# ---------------------------------------------------------
# RESUME ANALYZER (AI STYLE SCORING)
# ---------------------------------------------------------
def analyze_resume(text, user_id):

    raw = text.lower()
    score = 40   # base score
    suggestions = []

    # -------------------------------
    # 1️⃣ Keyword-based scoring
    # -------------------------------
    for category, words in KEYWORD_GROUPS.items():
        for w in words:
            if w in raw:
                score += 5

    # -------------------------------
    # 2️⃣ Check for key resume sections
    # -------------------------------
    sections = {
        "education": r"(education|qualification|degree)",
        "skills": r"(skills|technical skills|core skills)",
        "experience": r"(experience|internship|work history)",
        "projects": r"(project|case study|academic project)",
        "achievements": r"(achievement|award|certification)"
    }

    for section, pattern in sections.items():
        if not re.search(pattern, raw):
            suggestions.append(f"Add a section for {section.title()}.")
        else:
            score += 5

    # -------------------------------
    # 3️⃣ Check for metrics/achievements (AI rule)
    # -------------------------------
    if re.search(r"\b\d+%|\d{2,}", raw):
        score += 8   # measurable impact
    else:
        suggestions.append("Add measurable achievements (numbers, %, outcomes).")

    # -------------------------------
    # 4️⃣ Format & readability analysis
    # -------------------------------
    bullet_points = raw.count("•") + raw.count("- ")
    if bullet_points > 5:
        score += 5
    else:
        suggestions.append("Use bullet points to improve readability.")

    if len(raw.split(".")) > 20:
        score += 5  # good detailed resume

    # -------------------------------
    # 5️⃣ Detect missing commerce skills
    # -------------------------------
    essential = ["excel", "tally", "gst", "financial analysis", "communication"]

    for skill in essential:
        if skill not in raw:
            suggestions.append(f"Consider adding {skill.title()}.")

    # -------------------------------
    # Final scoring
    # -------------------------------
    score = min(score, 100)

    # -------------------------------
    # SAVE / UPDATE ResumeScore
    # -------------------------------
    existing = ResumeScore.query.filter_by(user_id=user_id).first()

    if not existing:
        result = ResumeScore(
            user_id=user_id,
            score=score,
            suggestions=json.dumps(suggestions)
        )
        db.session.add(result)
    else:
        existing.score = score
        existing.suggestions = json.dumps(suggestions)

    db.session.commit()

    return score, suggestions