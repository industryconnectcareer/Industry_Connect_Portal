import re

# -----------------------------
# COMMON STOPWORDS TO REMOVE
# -----------------------------
STOPWORDS = {
    "and", "skill", "skills", "proficient", "proficient in",
    "knowledge", "knowledge of", "basic", "advanced"
}

# -----------------------------
# SYNONYM NORMALIZATION
# -----------------------------
SKILL_SYNONYMS = {
    "ms excel": "excel",
    "microsoft excel": "excel",
    "advanced excel": "excel",
    "communication skills": "communication",
    "analytical ability": "analytical skills",
    "analysis": "analytical skills",
    "critical thinker": "critical thinking",
    "problem-solving": "problem solving",
    "data analysis": "data analytics",
    "stock market": "share market",
    "stock markets": "share markets",
    "income tax": "tax knowledge",
    "gst knowledge": "gst",
    "tally prime": "tally"
}

# -----------------------------
# CLEAN A SINGLE TEXT INPUT
# -----------------------------
def clean_text(t):
    if not t:
        return ""
    
    t = t.lower().strip()

    # Remove extra spaces
    t = re.sub(r"\s+", " ", t)

    # Remove stopwords
    for s in STOPWORDS:
        t = t.replace(s, "")

    t = t.strip()

    # Normalize synonyms
    if t in SKILL_SYNONYMS:
        t = SKILL_SYNONYMS[t]

    return t


# -----------------------------
# VECTORIZE SKILL STRING
# -----------------------------
def vectorize_skills(skill_str):
    if not skill_str:
        return []

    # Split by multiple separators: comma, slash, semicolon, pipe
    raw_parts = re.split(r"[,\;/|]+", skill_str)

    cleaned = []

    for part in raw_parts:
        part = clean_text(part)

        # Skip empty parts after cleaning
        if not part:
            continue

        # Normalize synonyms
        if part in SKILL_SYNONYMS:
            part = SKILL_SYNONYMS[part]

        cleaned.append(part)

    # Remove duplicates while maintaining order
    final_skills = list(dict.fromkeys(cleaned))

    return final_skills