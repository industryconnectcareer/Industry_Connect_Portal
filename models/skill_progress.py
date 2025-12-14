from datetime import datetime
from extensions import db

class SkillProgress(db.Model):
    __tablename__ = "skill_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    skill = db.Column(db.String(100), nullable=False)

    best_score = db.Column(db.Integer, default=0)
    attempts = db.Column(db.Integer, default=0)

    status = db.Column(db.String(20))  # Completed / Failed
    last_attempt = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("user_id", "skill"),
    )