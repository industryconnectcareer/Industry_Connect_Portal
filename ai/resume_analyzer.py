import re

# ----------------------------------------
# 1) Skill Categories & Synonyms
# ----------------------------------------
SKILL_MAP = {
    "excel": ["advanced excel", "ms excel", "spreadsheets"],
    "accounting": ["accounts", "bookkeeping", "accountancy"],
    "gst": ["tax", "taxation", "indirect tax"],
    "tally": ["tally prime", "erp9"],
    "finance": ["financial analysis", "finance modelling", "ratio analysis"],
    "communication": ["verbal communication", "presentation skills"],
    "analysis": ["data analysis", "analytical skills", "problem solving"]
}

# Combine synonyms into a flattened list for detection
ALL_KEYWORDS = list(SKILL_MAP.keys()) + [syn for sub in SKILL_MAP.values() for syn in sub]


# ----------------------------------------
# 2) Clean Text Function
# ----------------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)  # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()  # normalize spaces
    return text


# ----------------------------------------
# 3) Matching Logic (keyword + synonym)
# ----------------------------------------
def has_skill(text, skill):
    """Returns True if skill or any synonym appears in text."""

    if skill in text:
        return True

    if skill in SKILL_MAP:
        for syn in SKILL_MAP[skill]:
            if syn in text:
                return True

    return False


# ----------------------------------------
# 4) MAIN RESUME PARSER
# ----------------------------------------
def parse_resume(text):
    text = clean_text(text)

    base_score = 40   # minimum score
    score = base_score
    found_skills = []
    missing_skills = []

    # Weighted scoring system
    for skill in SKILL_MAP:
        if has_skill(text, skill):
            score += 10
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    # Cap score at 100
    score = min(score, 100)

    # ----------------------------------------
    # Generate Suggestions
    # ----------------------------------------
    suggestions = []

    for s in missing_skills:
        if s == "excel":
            suggestions.append("Add Advanced Excel or spreadsheet experience.")
        elif s == "gst":
            suggestions.append("Include GST/Taxation knowledge or practical exposure.")
        elif s == "tally":
            suggestions.append("Mention Tally Prime / ERP accounting experience.")
        elif s == "accounting":
            suggestions.append("Add accounting/bookkeeping concepts or experience.")
        elif s == "finance":
            suggestions.append("Add financial analysis or ratio analysis knowledge.")
        elif s == "communication":
            suggestions.append("Mention communication or presentation achievements.")
        elif s == "analysis":
            suggestions.append("Showcase analytical skills or problem-solving examples.")

    # Eliminate duplicates
    suggestions = list(set(suggestions))

    return {
        "score": score,
        "found_skills": found_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions
    }