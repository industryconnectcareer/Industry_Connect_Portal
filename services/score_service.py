from models.readiness_score import ReadinessScore
from models.resume_score import ResumeScore
from models.skill_badges import SkillBadge
from models.user import User

# 🔥 Commerce & Business Domain Skill Weights
HIGH_VALUE_SKILLS = [
    "excel", "advanced excel", "gst", "tally",
    "financial analysis", "data analysis", "taxation",
    "communication", "leadership", "analytics",
    "power bi", "sql", "financial modelling"
]


def compute_readiness_score(user_id):
    user = User.query.get(user_id)

    if not user:
        return {"total": 0, "breakdown": []}

    # ==================================================
    # 1️⃣ SKILLS SCORE (Max 40%)
    # ==================================================
    user_skills = [s.strip().lower() for s in (user.skills or "").split(",") if s.strip()]

    skill_score = 0

    for skill in user_skills:
        if skill in HIGH_VALUE_SKILLS:
            skill_score += 6
        else:
            skill_score += 3  # normal skill

    skill_score = min(skill_score, 40)

    # Penalty for very low skills
    if len(user_skills) < 3:
        skill_score -= 5

    # ==================================================
    # 2️⃣ RESUME SCORE (Max 25%)
    # ==================================================
    resume_obj = ResumeScore.query.filter_by(user_id=user_id).first()
    resume_score_raw = resume_obj.score if resume_obj else 0
    resume_score_weighted = (resume_score_raw / 100) * 25

    # ==================================================
    # 3️⃣ BADGES SCORE (Max 15%)
    # ==================================================
    badge_count = SkillBadge.query.filter_by(user_id=user_id).count()
    badge_score = min(badge_count * 5, 15)

    # ==================================================
    # 4️⃣ PROJECTS / TOOLS / EXPERIENCE SCORE (Max 10%)
    # ==================================================
    experience_score = 0

    if user.tools:
        tool_count = len(user.tools.split(","))
        experience_score += min(tool_count * 2, 6)

    if "project" in (user.bio or "").lower():
        experience_score += 4

    experience_score = min(experience_score, 10)

    # ==================================================
    # 5️⃣ MCQ / ASSESSMENT SCORE (Max 10%) — future logic
    # ==================================================
    test_score = 10  # Default until MCQ module added

    # ==================================================
    # TOTAL SCORE
    # ==================================================
    total_score = skill_score + resume_score_weighted + badge_score + experience_score + test_score
    total_score = int(min(total_score, 100))

    breakdown = [
        {"name": "Skills", "value": int(skill_score), "max": 40},
        {"name": "Resume Score", "value": int(resume_score_weighted), "max": 25},
        {"name": "Badges Earned", "value": int(badge_score), "max": 15},
        {"name": "Projects & Tools", "value": int(experience_score), "max": 10},
        {"name": "MCQ / Test", "value": int(test_score), "max": 10},
    ]

    # ==================================================
    # Save in DB (auto update)
    # ==================================================
    ReadinessScore.compute_and_save(
        user_id=user_id,
        total=total_score,
        breakdown=breakdown
    )

    return {
        "total": total_score,
        "breakdown": breakdown
    }