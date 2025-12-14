from models.internship import Internship
from models.user import User


# ----------------------------------------------------------
# Helper: Clean & normalize skill strings
# ----------------------------------------------------------
def normalize_skills(skill_str):
    if not skill_str:
        return []
    return [s.strip().lower() for s in skill_str.split(",") if s.strip()]


# ----------------------------------------------------------
# AI-Enhanced Match Score Calculation
# ----------------------------------------------------------
def match_score(internship, student):
    score = 0

    student_skills = normalize_skills(student.skills)
    internship_skills = normalize_skills(internship.skills)

    # ---------------------------------------------
    # 1️⃣ SKILL MATCHING (Primary Weight)
    # ---------------------------------------------
    for ss in student_skills:
        for iskill in internship_skills:
            if ss in iskill:   # partial matching (better)
                score += 12     # Increased weight
                break

    # Max cap for skills → 70
    score = min(score, 70)

    # ---------------------------------------------
    # 2️⃣ LOCATION MATCH
    # ---------------------------------------------
    if student.location and internship.location:
        if student.location.lower().strip() == internship.location.lower().strip():
            score += 10

    # ---------------------------------------------
    # 3️⃣ MODE MATCH (Online / Offline / Hybrid)
    # ---------------------------------------------
    if hasattr(student, "preferred_mode") and student.preferred_mode:
        if internship.mode.lower() == student.preferred_mode.lower():
            score += 8

    # ---------------------------------------------
    # 4️⃣ CATEGORY MATCH (Finance, Taxation, etc.)
    # ---------------------------------------------
    if hasattr(student, "course") and student.course:
        if student.course.lower() in (internship.category or "").lower():
            score += 10

    # ---------------------------------------------
    # 5️⃣ PAID INTERNSHIP PREFERENCE
    # ---------------------------------------------
    if internship.is_paid:
        score += 5

    return min(score, 100)


# ----------------------------------------------------------
# Get Top Internship Recommendations
# ----------------------------------------------------------
def get_recommendations(student, limit=10):
    internships = Internship.query.filter_by(status="Approved").all()
    scored = []

    for internship in internships:
        score = match_score(internship, student)

        # Soft threshold to avoid showing irrelevant internships
        if score >= 25:
            scored.append((internship, score))

    # Sort highest score first
    scored.sort(key=lambda x: x[1], reverse=True)

    # Return only internship objects in sorted order
    return [item[0] for item in scored[:limit]]