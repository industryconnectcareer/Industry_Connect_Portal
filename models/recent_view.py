# models/recent_view.py

from app import db
from datetime import datetime

class RecentView(db.Model):
    __tablename__ = "recent_views"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey("internships.id"), nullable=False)

    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to Internship
    internship = db.relationship(
    "Internship",
    backref="recent_views",
    foreign_keys="RecentView.internship_id"
    )

    def __repr__(self):
        return f"<RecentView user={self.user_id} internship={self.internship_id}>"