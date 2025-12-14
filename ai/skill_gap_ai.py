import re

# ---------------------------------------------
# SKILL GROUPS & SYNONYMS (improved coverage)
# ---------------------------------------------
SKILL_GROUPS = {
    "communication": ["verbal communication", "presentation", "public speaking", "spoken english"],
    "analytical skills": ["analysis", "data analysis", "problem solving", "critical thinking"],
    "mathematical skills": ["math", "statistics", "quantitative"],
    "accounting skills": ["accounting", "bookkeeping", "ledger", "journal"],
    "business interest": ["business", "commerce", "management"],
    "leadership skills": ["leadership", "team lead", "coordination", "team management"],
    "critical thinking": ["logic", "decision making", "reasoning"],
    "economics": ["economic", "microeconomics", "macroeconomics"],
    "finance modelling": ["financial modelling", "valuation", "forecasting"],
    "financial analysis": ["ratio analysis", "trend analysis", "valuation", "financial review"],
    "innovation skills": ["creativity", "innovation", "idea generation"],
    "problem solving": ["troubleshooting", "analytical problem solving"],
    "share markets": ["stock market", "trading", "nifty", "sensex"],
    "computer literacy": ["computer skills", "ms office", "typing", "basic computer"],
    "data analysis": ["analytics", "power bi", "excel analysis"],
    "excel": ["advanced excel", "ms excel", "spreadsheets"],
    "financial literacy": ["budgeting", "savings", "investments"],
    "knowledge about taxes": ["gst", "income tax", "tds", "taxation"],
    "tax consultant": ["tax advisor", "tax filing", "ca assistant"],
    "tally": ["tally prime", "erp9", "tally erp9"],
}

# ---------------------------------------------
# CAREER ROLE MAPPING (improved accuracy)
# ---------------------------------------------
ROLE_MAP = {
    "chartered accountant": ["accounting skills", "knowledge about taxes", "tally"],
    "company secretary": ["communication", "business interest", "law"],
    "financial analyst": ["financial analysis", "excel", "finance modelling"],
    "actuary": ["mathematical skills", "statistics", "analysis"],
    "human resources": ["communication", "leadership skills"],
    "investment banking": ["finance modelling", "excel", "economics"],
    "management accountant": ["accounting skills", "costing", "analysis"],
    "digital marketing": ["marketing", "communication", "computer literacy"],
    "economist": ["economics", "mathematical skills"],
    "entrepreneur": ["business interest", "leadership skills"],
    "bank manager": ["communication", "financial literacy"],
    "cost accountant": ["accounting skills", "analysis"],
    "sales manager": ["communication", "business interest"],
    "tax advisor": ["knowledge about taxes", "gst"],
    "bba careers": ["business interest", "communication"],
    "cpa": ["accounting skills"],
    "e-commerce": ["digital marketing", "computer literacy"],
    "legal (LLB)": ["law", "communication"],
    "marketing manager": ["communication", "digital marketing"],
    "accountant": ["accounting skills", "tally"],
}

# ---------------------------------------------
# CLEAN TEXT
# ---------------------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

# ---------------------------------------------
# MAIN RESUME PARSER FUNCTION
# ---------------------------------------------
def parse_resume(text):
    text = clean_text(text)

    score = 40  # Base score
    found_skills = []
    missing_skills = []

    # -----------------------------------------
    # SKILL MATCHING + SCORING
    # -----------------------------------------
    for skill, synonyms in SKILL_GROUPS.items():
        matched = False

        # Direct match
        if skill in text:
            matched = True

        # Synonym match
        for syn in synonyms:
            if syn in text:
                matched = True
                break

        if matched:
            found_skills.append(skill)
            score += 5
        else:
            missing_skills.append(skill)

    # Score limit
    score = min(score, 100)

    # -----------------------------------------
    # CAREER ROLE PREDICTION
    # -----------------------------------------
    matched_roles = []

    for role, required_skills in ROLE_MAP.items():
        match_count = sum(1 for s in required_skills if s in found_skills)
        threshold = max(1, len(required_skills) // 2)  # 50% of required skills

        if match_count >= threshold:
            matched_roles.append(role)

    if not matched_roles:
        matched_roles.append("General Commerce Role")

    # -----------------------------------------
    # SUGGESTIONS
    # -----------------------------------------
    suggestions = [
        f"Improve your resume by adding: {s.capitalize()}."
        for s in missing_skills[:10]
    ]

    return {
        "score": score,
        "found_skills": sorted(found_skills),
        "missing_skills": sorted(missing_skills),
        "suggestions": suggestions,
        "recommended_roles": matched_roles,
    }


# ---------------------------------------------
# SKILL GAP FUNCTION USED IN INTERNSHIP MATCHING
# ---------------------------------------------
def analyze_skill_gap(user_skills, required_skills):
    """
    Analyze skill gap based on user's skills vs. required skills.

    user_skills → list of skills student has
    required_skills → list of skills internship requires
    """

    results = []

    for skill in required_skills:
        match = 100 if skill in user_skills else 40  # basic scoring logic
        
        results.append({
            "skill": skill,
            "match": match
        })

    # Recommended courses for skills not matched
    recommendations = [
        f"Course for {skill}" for skill in required_skills if skill not in user_skills
    ]

    return results, recommendations