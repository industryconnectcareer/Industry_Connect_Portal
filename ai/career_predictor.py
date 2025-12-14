def predict_role(skills):
    if not skills:
        return ["General Commerce Role"]

    skills = [s.lower().strip() for s in skills]
    text = " ".join(skills)

    # ================================================
    # CAREER ROLES + SKILL MAPPING
    # ================================================
    role_rules = {
        "Chartered Accountant (CA)": [
            "accounting", "accounting skills", "tally", "journal", "ledger",
            "mathematical skills", "financial statements", "audit"
        ],

        "Company Secretary (CS)": [
            "law", "llb", "compliance", "corporate law", "management"
        ],

        "Financial Analyst": [
            "financial analysis", "finance modelling", "excel", "advanced excel",
            "economics", "analytical skills", "problem solving", "critical thinking",
            "financial literacy", "data analysis"
        ],

        "Actuary": [
            "mathematical skills", "statistics", "probability", "analytical skills"
        ],

        "Human Resources (HR)": [
            "communication", "leadership skills", "team handling",
            "presentation", "interpersonal"
        ],

        "Investment Banking": [
            "finance", "financial modelling", "share markets", "valuation",
            "investment", "equity", "portfolio"
        ],

        "Management Accountant (CMA)": [
            "cost accounting", "accounting skills", "mathematical skills",
            "finance", "excel"
        ],

        "Digital Marketing Specialist": [
            "marketing", "social media", "innovation skills",
            "communication", "business interest"
        ],

        "Economist": [
            "economics", "data analysis", "critical thinking", "financial literacy"
        ],

        "Entrepreneurship": [
            "business interest", "innovation skills", "leadership",
            "problem solving", "management"
        ],

        "Bank Manager": [
            "financial literacy", "communication", "management",
            "customer service"
        ],

        "Cost Accountant": [
            "mathematical skills", "accounting skills", "finance",
            "analysis", "costing"
        ],

        "Sales Manager": [
            "communication", "leadership", "sales", "business interest",
            "marketing"
        ],

        "Tax Advisor / Consultant": [
            "tax", "knowledge about taxes", "tax consultant",
            "gst", "return filing"
        ],

        "BBA (Business Administration)": [
            "management", "leadership", "communication",
            "business interest"
        ],

        "Certified Public Accountant (CPA)": [
            "accounting", "financial analysis", "audit", "excel"
        ],

        "E-Commerce Specialist": [
            "e-commerce", "digital marketing", "business interest",
            "computer literacy"
        ],

        "Legal Advisor (LLB)": [
            "llb", "law", "compliance", "corporate law"
        ],

        "Marketing Manager": [
            "marketing", "communication", "creativity", "innovation skills"
        ],

        "General Accountant": [
            "accounting", "tally", "bookkeeping", "mathematical skills"
        ]
    }

    predicted_roles = set()

    # FIND MATCHES BASED ON SKILLS
    for role, keywords in role_rules.items():
        for kw in keywords:
            if kw in text:
                predicted_roles.add(role)
                break

    return list(predicted_roles) or ["General Commerce Role"]