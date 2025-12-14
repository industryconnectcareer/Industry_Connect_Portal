from models.internship import Internship
from models.ojt import OJT
from ai.preprocessing import vectorize_skills


# --------------------------------------------------
# SYNONYM MAP (extend easily)
# --------------------------------------------------
SYNONYMS = {
    "communication": ["communication skills", "verbal communication", "spoken english"],
    "excel": ["advanced excel", "ms excel", "microsoft excel"],
    "problem solving": ["problem-solving", "critical thinking", "analytical skills"],
    "financial analysis": ["finance modelling", "ratio analysis"],
    "tax": ["gst", "income tax", "tax consultant", "taxation"]
}


# --------------------------------------------------
# MATCHING FUNCTION WITH PARTIAL + SYNONYM MATCHING
# --------------------------------------------------
def skill_match(skill, skill_list):
    """Returns True if skill appears directly, partially, or via synonyms."""

    skill = skill.lower().strip()

    # Direct match
    if skill in skill_list:
        return True

    # Partial match
    for s in skill_list:
        if skill in s or s in skill:
            return True

    # Synonym match
    if skill in SYNONYMS:
        for syn in SYNONYMS[skill]:
            if syn in skill_list:
                return True

    return False


# --------------------------------------------------
# SIMILARITY SCORE ENGINE
# --------------------------------------------------
def compute_similarity(student_vec, intern_vec):
    if not student_vec or not intern_vec:
        return 0

    score = 0
    weight = 10  # base weight per matched skill

    for skill in student_vec:
        if skill_match(skill, intern_vec):
            score += weight

    # Normalize score (max 100)
    return min(score, 100)


# --------------------------------------------------
# INTERNSHIP RECOMMENDATION ENGINE
# --------------------------------------------------
def recommend_internships(student):
    """Recommend internships based on student's skills."""
    
    student_vec = vectorize_skills(student.skills or "")
    internships = Internship.query.filter_by(status="Approved").all()

    scored = []

    for intern in internships:
        intern_vec = vectorize_skills(intern.skills or "")
        score = compute_similarity(student_vec, intern_vec)

        scored.append({
            "item": intern,
            "score": score,
            "match_count": sum(1 for s in student_vec if skill_match(s, intern_vec))
        })

    # Sort by → score → match count → latest
    scored.sort(key=lambda x: (x["score"], x["match_count"], x["item"].id), reverse=True)

    # Return internship objects only
    return [x["item"] for x in scored[:10]]


# --------------------------------------------------
# OJT RECOMMENDATION ENGINE
# --------------------------------------------------
def recommend_ojts(student):
    """Recommend OJT programs based on student's skills."""
    
    student_vec = vectorize_skills(student.skills or "")
    ojts = OJT.query.filter_by(status="Approved").all()

    scored = []

    for ojt in ojts:
        ojt_vec = vectorize_skills(ojt.skills or "")
        score = compute_similarity(student_vec, ojt_vec)

        scored.append({
            "item": ojt,
            "score": score,
            "match_count": sum(1 for s in student_vec if skill_match(s, ojt_vec))
        })

    # Sort by score → match count → latest
    scored.sort(key=lambda x: (x["score"], x["match_count"], x["item"].id), reverse=True)

    # Return OJT objects only
    return [x["item"] for x in scored[:10]]