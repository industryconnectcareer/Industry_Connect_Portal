# models/readiness_score.py
from datetime import datetime
from app import db
import json


class ReadinessScore(db.Model):
    __tablename__ = "readiness_scores"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)

    score = db.Column(db.Integer, default=0)               # total readiness score
    breakdown = db.Column(db.Text, nullable=True)         # JSON: scoring split
    suggestions = db.Column(db.Text, nullable=True)       # JSON: personalized suggestions
    history = db.Column(db.Text, default="[]")            # JSON list of past scores

    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ---------------------------------------------------------
    # GET CURRENT SCORE
    # ---------------------------------------------------------
    @staticmethod
    def get_score(user_id):
        obj = ReadinessScore.query.filter_by(user_id=user_id).first()
        return obj.score if obj else 0

    # ---------------------------------------------------------
    # SAVE / UPDATE SCORE + BREAKDOWN + SUGGESTIONS
    # ---------------------------------------------------------
    @staticmethod
    def save(user_id, total, breakdown, suggestions):
        obj = ReadinessScore.query.filter_by(user_id=user_id).first()

        if not obj:
            obj = ReadinessScore(user_id=user_id)

        # Save history (keeps last 10 entries)
        history = obj.get_history()
        history.append({"score": total, "date": datetime.utcnow().isoformat()})
        history = history[-10:]

        obj.score = int(total)
        obj.breakdown = json.dumps(breakdown)
        obj.suggestions = json.dumps(suggestions)
        obj.history = json.dumps(history)
        obj.updated_at = datetime.utcnow()

        db.session.add(obj)
        db.session.commit()
        return obj

    # ---------------------------------------------------------
    # JSON HELPERS
    # ---------------------------------------------------------
    def get_breakdown(self):
        return json.loads(self.breakdown) if self.breakdown else {}

    def get_suggestions(self):
        return json.loads(self.suggestions) if self.suggestions else []

    def get_history(self):
        try:
            return json.loads(self.history)
        except:
            return []

    # ---------------------------------------------------------
    # SMART READINESS ENGINE (COMPUTE SCORE)
    # ---------------------------------------------------------
    @staticmethod
    def compute(user):
        """
        Calculates career readiness score based on:
        - Skills
        - Tools
        - Applications
        - Resume score
        - Mock interview score (future integration)
        """

        # ------------- Skills Score -------------
        skills = (user.skills or "").split(",")
        skill_score = min(len([s for s in skills if s.strip()]), 10) * 5  # Max 50

        # ------------- Tools Score -------------
        tools = (user.tools or "").split(",")
        tool_score = min(len([t for t in tools if t.strip()]), 6) * 5      # Max 30

        # ------------- Internship Activity -------------
        from models.applications import Application
        applied = Application.query.filter_by(user_id=user.id).count()
        activity_score = min(applied * 5, 25)

        # ------------- Resume Score -------------
        from models.resume_score import ResumeScore
        resume_obj = ResumeScore.query.filter_by(user_id=user.id).first()
        resume_score = resume_obj.score if resume_obj else 0
        resume_score = min(resume_score / 2, 25)

        # -------- Total Score (out of 100) --------
        total = skill_score + tool_score + activity_score + resume_score
        total = min(int(total), 100)

        # -------- Breakdown --------
        breakdown = {
            "skills": skill_score,
            "tools": tool_score,
            "applications": activity_score,
            "resume_quality": resume_score
        }

        # -------- Suggestions --------
        suggestions = []

        if skill_score < 40:
            suggestions.append("Add more commerce-specific skills such as GST, Excel, Tally, and Finance Analysis.")

        if tool_score < 20:
            suggestions.append("Improve your toolset: Power BI, Excel, Tally, Google Sheets.")

        if activity_score < 15:
            suggestions.append("Apply for more internships to improve practical exposure.")

        if resume_score < 20:
            suggestions.append("Update your resume to improve formatting, achievements, and clarity.")

        return {
            "total": total,
            "breakdown": breakdown,
            "suggestions": suggestions,
        }