# models/skill_gap.py
from datetime import datetime
from app import db
import json


class SkillGap(db.Model):
    __tablename__ = "skill_gaps"

    id = db.Column(db.Integer, primary_key=True)

    # Student reference
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Target career role (e.g., Financial Analyst, CA, HR Manager)
    role = db.Column(db.String(180), nullable=False, index=True)

    # JSON fields
    missing_skills = db.Column(db.Text, nullable=True)     # JSON list
    matched_skills = db.Column(db.Text, nullable=True)     # JSON list

    # Percentage match between student profile & expected skills
    match_percent = db.Column(db.Integer, default=0)

    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Ensure each user can have only ONE skill gap analysis per role
    __table_args__ = (
        db.UniqueConstraint("user_id", "role", name="unique_skill_gap_per_role"),
    )

    # --------------------------------------------------------------
    # JSON helpers
    # --------------------------------------------------------------
    def missing_list(self):
        try:
            return json.loads(self.missing_skills) if self.missing_skills else []
        except:
            return []

    def matched_list(self):
        try:
            return json.loads(self.matched_skills) if self.matched_skills else []
        except:
            return []

    # --------------------------------------------------------------
    # Update the model with new results
    # --------------------------------------------------------------
    def update_gap(self, missing, matched, match_percent):
        self.missing_skills = json.dumps(missing)
        self.matched_skills = json.dumps(matched)
        self.match_percent = int(match_percent)
        self.analyzed_at = datetime.utcnow()

    # --------------------------------------------------------------
    # Convert row → dictionary for dashboards / APIs
    # --------------------------------------------------------------
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "role": self.role,
            "missing_skills": self.missing_list(),
            "matched_skills": self.matched_list(),
            "match_percent": self.match_percent,
            "analyzed_at": self.analyzed_at.strftime("%Y-%m-%d"),
        }

    def __repr__(self):
        return f"<SkillGap user:{self.user_id} role:{self.role} match:{self.match_percent}%>"