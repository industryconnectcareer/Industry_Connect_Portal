from datetime import datetime
from extensions import db


class Placement(db.Model):
    __tablename__ = "placements"

    id = db.Column(db.Integer, primary_key=True)

    # Relations
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    college_id = db.Column(
        db.Integer,
        db.ForeignKey("colleges.id"),
        nullable=False
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    # Academic info
    academic_year = db.Column(
        db.String(20),  # FY / SY / TY / PART1 / PART2
        nullable=False
    )

    # Placement details
    company = db.Column(db.String(180), nullable=False)
    role = db.Column(db.String(150), nullable=True)
    package = db.Column(db.Float, nullable=True)  # LPA
    placed_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Status
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Placement {self.company} | {self.academic_year}>"
    
class InternshipMatch(db.Model):
    __tablename__ = "internship_matches"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    internship_id = db.Column(db.Integer, db.ForeignKey("internships.id"))

    match_score = db.Column(db.Integer)
    skill_match = db.Column(db.Integer)
    location_match = db.Column(db.Integer)
    department_match = db.Column(db.Integer)