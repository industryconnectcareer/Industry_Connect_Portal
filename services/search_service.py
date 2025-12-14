from models.saved_search import SavedSearch
from models.internship import Internship
from sqlalchemy import or_, and_

def run_saved_searches(user_id):
    searches = SavedSearch.query.filter_by(user_id=user_id).all()
    results = set()   # use a set to avoid duplicates

    for s in searches:

        query_text = (s.query or "").strip().lower()
        category = (s.category or "").strip().lower()
        mode = (s.mode or "").strip().lower()

        # -------------------------------------------
        # BASE QUERY → only approved internships
        # -------------------------------------------
        q = Internship.query.filter(Internship.status == "Approved")

        # -------------------------------------------
        # TEXT SEARCH: title, skills, category, company
        # -------------------------------------------
        if query_text:
            q = q.filter(or_(
                Internship.title.ilike(f"%{query_text}%"),
                Internship.skills.ilike(f"%{query_text}%"),
                Internship.company.ilike(f"%{query_text}%"),
                Internship.category.ilike(f"%{query_text}%")
            ))

        # -------------------------------------------
        # CATEGORY FILTER
        # -------------------------------------------
        if category:
            q = q.filter(Internship.category.ilike(f"%{category}%"))

        # -------------------------------------------
        # MODE FILTER (Remote / Offline / Hybrid)
        # -------------------------------------------
        if mode:
            q = q.filter(Internship.mode.ilike(f"%{mode}%"))

        # -------------------------------------------
        # Add matches to result set
        # -------------------------------------------
        for intern in q.all():
            results.add(intern)

    # -------------------------------------------
    # Convert set → list and sort by relevance
    # -------------------------------------------
    def relevance_score(i):
        score = 0

        # Ranking alphabetically by title improves UX
        if i.title:
            score += 1

        # Give weight if internship contains keywords from saved searches
        for s in searches:
            if s.query and s.query.lower() in (i.title.lower() + i.skills.lower()):
                score += 5

        return score

    sorted_results = sorted(list(results), key=relevance_score, reverse=True)

    return sorted_results