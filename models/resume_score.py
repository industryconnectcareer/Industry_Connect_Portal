# models/resume_score.py
from datetime import datetime
from app import db
import json


class ResumeScore(db.Model):
    __tablename__ = "resume_scores"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)

    score = db.Column(db.Integer, default=0)                     # Final ATS score
    breakdown = db.Column(db.Text, nullable=True)               # JSON -> detailed scoring
    suggestions = db.Column(db.Text, nullable=True)             # JSON -> improvement tips
    missing_keywords = db.Column(db.Text, nullable=True)        # JSON -> lacking skills/terms
    history = db.Column(db.Text, default="[]")                  # JSON list of past evaluations

    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)

    # -----------------------------------------------------
    # JSON HELPERS
    # -----------------------------------------------------
    def suggestions_list(self):
        return json.loads(self.suggestions) if self.suggestions else []

    def breakdown_dict(self):
        return json.loads(self.breakdown) if self.breakdown else {}

    def missing_keywords_list(self):
        return json.loads(self.missing_keywords) if self.missing_keywords else []

    def history_list(self):
        try:
            return json.loads(self.history)
        except:
            return []

    # -----------------------------------------------------
    # CREATE / UPDATE RESUME SCORE
    # -----------------------------------------------------
    @staticmethod
    def save(user_id, score, breakdown, suggestions, missing_keywords):
        obj = ResumeScore.query.filter_by(user_id=user_id).first()

        if not obj:
            obj = ResumeScore(user_id=user_id)

        # --- Save history (max 10 items) ---
        history = obj.history_list()
        history.append({
            "score": score,
            "date": datetime.utcnow().isoformat()
        })
        history = history[-10:]

        obj.score = int(score)
        obj.breakdown = json.dumps(breakdown)
        obj.suggestions = json.dumps(suggestions)
        obj.missing_keywords = json.dumps(missing_keywords)
        obj.history = json.dumps(history)
        obj.analyzed_at = datetime.utcnow()

        db.session.add(obj)
        db.session.commit()

        return obj

    # -----------------------------------------------------
    # AI-BASED RESUME SCORE CALCULATION LOGIC
    # -----------------------------------------------------
    @staticmethod
    def compute(text):
        """
        You can expand this logic or connect NLP/AI later.
        """

        text = text.lower()

        # Commerce & business keywords
        keywords = [
            "tally", "gst", "excel", "power bi", "analysis", "finance",
            "accounting", "management", "banking", "tax", "auditing",
            "financial modelling", "communication", "leadership"
        ]

        found = [k for k in keywords if k in text]
        missing = [k for k in keywords if k not in text]

        # Simple scoring logic
        score = 40 + len(found) * 4    # Base score + keyword coverage
        score = min(score, 100)

        breakdown = {
            "keywords_matched": len(found) * 4,
            "base_score": 40,
            "coverage": f"{len(found)}/{len(keywords)}"
        }

        suggestions = []
        if len(found) < 6:
            suggestions.append("Add more commerce-related keywords to improve ATS compatibility.")

        if "excel" not in found:
            suggestions.append("Mention Excel or Advanced Excel proficiency.")

        if "gst" not in found:
            suggestions.append("Include GST or taxation experience.")

        if "tally" not in found:
            suggestions.append("Mention hands-on work with Tally.")

        return score, breakdown, suggestions, missing

    def __repr__(self):
        return f"<ResumeScore user:{self.user_id} score:{self.score}>"