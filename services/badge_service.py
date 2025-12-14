from models.skill_badges import SkillBadge
from app import db


# --------------------------------------------------------------
# 🔥 Badge Dictionary (Expandable)
# --------------------------------------------------------------
BADGE_RULES = {
    "tally": {
        "name": "Tally Specialist",
        "icon": "badge_tally.png",
        "keywords": ["tally", "erp9", "tally prime"],
        "level": "Intermediate",
    },
    "gst": {
        "name": "GST Practitioner",
        "icon": "badge_gst.png",
        "keywords": ["gst", "taxation", "indirect tax", "gstr"],
        "level": "Intermediate",
    },
    "excel": {
        "name": "Excel Specialist",
        "icon": "badge_excel.png",
        "keywords": ["excel", "advanced excel", "pivot", "vlookup", "power query"],
        "level": "Expert",
    },
    "finance": {
        "name": "Finance Analyst",
        "icon": "badge_finance.png",
        "keywords": ["finance", "financial analysis", "financial modelling"],
        "level": "Expert",
    },
    "communication": {
        "name": "Communication Pro",
        "icon": "badge_communication.png",
        "keywords": ["communication", "presentation", "public speaking"],
        "level": "Beginner",
    },
    "analytics": {
        "name": "Analytics Explorer",
        "icon": "badge_analytics.png",
        "keywords": ["analytics", "data analysis", "power bi"],
        "level": "Intermediate",
    },
    "accounting": {
        "name": "Accounting Basics",
        "icon": "badge_accounting.png",
        "keywords": ["accounting", "ledger", "journal", "balance sheet"],
        "level": "Beginner",
    },
    "tax": {
        "name": "Tax Advisor",
        "icon": "badge_tax.png",
        "keywords": ["tax", "income tax", "tds", "itr"],
        "level": "Intermediate",
    },
    "stock": {
        "name": "Share Market Enthusiast",
        "icon": "badge_stock.png",
        "keywords": ["stock", "trading", "nifty", "sensex", "equity"],
        "level": "Beginner",
    },
    "leadership": {
        "name": "Leadership Learner",
        "icon": "badge_leadership.png",
        "keywords": ["leadership", "teamwork", "management"],
        "level": "Beginner",
    },
    "maths": {
        "name": "Mathematical Thinker",
        "icon": "badge_math.png",
        "keywords": ["math", "mathematical", "quantitative"],
        "level": "Intermediate",
    }
}


# --------------------------------------------------------------
# 🧠 SMART BADGE DETECTION ENGINE
# --------------------------------------------------------------
def check_and_award_badges(user):

    if not user.skills:
        return

    skills = [s.strip().lower() for s in user.skills.split(",")]

    for key, rule in BADGE_RULES.items():
        if skill_matches(skills, rule["keywords"]):
            award_badge(
                user_id=user.id,
                name=rule["name"],
                icon=rule["icon"],
                level=rule["level"],
            )


# --------------------------------------------------------------
# 🔍 Flexible Matching (synonyms + partials)
# --------------------------------------------------------------
def skill_matches(skills, keywords):
    for skill in skills:
        for key in keywords:
            if key in skill:  # partial match support
                return True
    return False


# --------------------------------------------------------------
# 🏅 Award Badge (Prevents duplicates)
# --------------------------------------------------------------
def award_badge(user_id, name, icon, level):
    exists = SkillBadge.query.filter_by(user_id=user_id, name=name).first()
    if exists:
        return

    badge = SkillBadge(
        user_id=user_id,
        name=name,
        icon=icon,
        level=level  # Added level support
    )
    db.session.add(badge)
    db.session.commit()