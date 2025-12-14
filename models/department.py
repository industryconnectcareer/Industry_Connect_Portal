from datetime import datetime
from extensions import db


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)

    # Department info
    name = db.Column(db.String(120), nullable=False)

    # Relationship
    college_id = db.Column(
        db.Integer,
        db.ForeignKey("colleges.id"),
        nullable=False
    )

    # Meta
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Department {self.name}>"