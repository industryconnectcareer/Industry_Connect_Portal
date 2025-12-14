import random

# ============================================================
# 1) MASTER QUESTION BANK (Commerce + Skills + Career Roles)
# ============================================================

questions = [
    # Accounting & Finance
    "Explain the difference between Journal and Ledger.",
    "What is GST? Why is it important?",
    "What are the components of a Balance Sheet?",
    "Difference between Accounts Payable and Accounts Receivable?",
    "Explain Tally Prime features.",
    "Explain the difference between capital expenditure and revenue expenditure.",
    "What is depreciation? Give examples.",
    "What is working capital? Why is it important?",
    "Explain the accounting equation with examples.",
    
    # Financial Analysis / Analyst Roles
    "What is financial modelling?",
    "Explain DCF valuation.",
    "What is EBITDA?",
    "How do you analyze a company’s performance?",
    "What is ratio analysis?",

    # Economics
    "What is inflation? Explain its impact.",
    "Explain GDP and GNP.",
    "What causes recession?",

    # Stock Market
    "Difference between primary and secondary markets.",
    "What is an index fund?",
    "Explain risk vs return.",

    # Business Skills
    "Explain critical thinking with an example.",
    "Describe a time you solved a major problem.",
    "Explain leadership in your own words.",
    
    # Taxation
    "What is input tax credit?",
    "Difference between tax planning and tax evasion.",

    # Excel / Data Skills
    "What is VLOOKUP? When do you use it?",
    "Explain pivot tables with an example.",
    "What is data cleaning?",

    # Communication / HR
    "How do you handle conflict in a team?",
    "Explain effective communication with an example.",
]

# ============================================================
# 2) KEYWORD DICTIONARY FOR SMART SCORING
# ============================================================

keywords = {
    "journal": ["debit", "credit", "transactions", "chronological"],
    "ledger": ["posting", "classification", "accounts"],
    "gst": ["tax", "input tax credit", "output tax", "indirect tax"],
    "balance sheet": ["assets", "liabilities", "equity", "financial position"],
    "accounts payable": ["creditors", "liability", "suppliers"],
    "accounts receivable": ["debtors", "asset", "customers"],
    "financial modelling": ["excel", "forecast", "valuation", "assumptions"],
    "dcf": ["discount rate", "cash flow", "terminal value", "valuation"],
    "ebitda": ["earnings", "interest", "tax", "depreciation"],
    "ratio analysis": ["liquidity", "profitability", "solvency"],
    "inflation": ["price rise", "purchasing power", "demand"],
    "gdp": ["economic output", "growth", "market value"],
    "index": ["nifty", "sensex", "basket of stocks"],
    "itc": ["input tax credit", "gst", "claim"],
    "vlookup": ["lookup", "excel", "match"],
    "pivot": ["summarize", "tables", "excel"],
    "communication": ["listening", "clarity", "verbal"],
    "leadership": ["motivate", "team", "responsibility"],
    "problem": ["solution", "analysis", "identify"]
}

# ============================================================
# 3) QUESTION GENERATOR
# ============================================================

def generate_question():
    return random.choice(questions)

# ============================================================
# 4) SMART ANSWER EVALUATOR
# ============================================================

def evaluate_answer(question, answer):
    answer = answer.lower().strip()

    # Basic length check
    if len(answer) < 25:
        return {
            "score": 10,
            "feedback": "Your answer is too short. Try adding examples, definitions, and clarity."
        }

    # Keyword scoring
    score = 0
    matched_keywords = []

    for key, kw_list in keywords.items():
        if key in question.lower():  
            for kw in kw_list:
                if kw.lower() in answer:
                    score += 10
                    matched_keywords.append(kw)

    # Depth scoring
    if len(answer.split()) > 80:
        score += 10  # bonus for detailed explanation

    # Generate feedback
    if score < 30:
        feedback = "Fair attempt. Add more concepts, definitions, and examples."
    elif score < 60:
        feedback = "Good answer! You covered some important points. Add depth and examples."
    else:
        feedback = "Excellent answer! You explained key concepts very clearly."

    return {
        "score": min(score, 100),
        "matched_keywords": matched_keywords,
        "feedback": feedback
    }

# ============================================================
# 5) HINT GENERATOR
# ============================================================

def get_hint(question):
    """
    Return a small hint based on the question topic.
    """
    q = question.lower()

    if "journal" in q:
        return "Hint: Think about chronological recording of transactions."
    if "ledger" in q:
        return "Hint: Ledger involves classification into accounts."
    if "gst" in q:
        return "Hint: Mention input/output tax and indirect tax."
    if "balance sheet" in q:
        return "Hint: It includes assets, liabilities, and equity."
    if "working capital" in q:
        return "Hint: It's current assets minus current liabilities."

    return "Think of key definitions, examples, and real use cases."

# ============================================================
# 6) FOLLOW-UP QUESTION GENERATOR
# ============================================================

def get_followup_question(question):
    """
    Generates a follow-up question based on the main question.
    """
    q = question.lower()

    if "journal" in q:
        return "Can you explain one example of a journal entry?"
    if "ledger" in q:
        return "How does ledger posting help in preparing the trial balance?"
    if "gst" in q:
        return "What is the difference between CGST and SGST?"
    if "balance sheet" in q:
        return "Why must assets always equal liabilities + equity?"
    if "inflation" in q:
        return "How can inflation be controlled?"
    if "vlookup" in q:
        return "When should XLOOKUP be preferred over VLOOKUP?"
    if "communication" in q:
        return "How do you ensure clarity when speaking to a team?"
    if "leadership" in q:
        return "What leadership style do you follow?"

    # Default follow-up
    return "Can you elaborate further with an example?"
