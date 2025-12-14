from datetime import datetime
from app import db

class ApplicationHistory(db.Model):
    __tablename__ = "application_history"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer,
        db.ForeignKey("applications.id"),
        nullable=False
    )

    old_status = db.Column(db.String(40))
    new_status = db.Column(db.String(40))

    changed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AppHistory app:{self.application_id} {self.old_status} → {self.new_status}>"