# models/ojt.py
from datetime import datetime
from app import db


class OJT(db.Model):
    __tablename__ = "ojt_programs"

    id = db.Column(db.Integer, primary_key=True)

    # -----------------------------
    # BASIC DETAILS
    # -----------------------------
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True)

    company_name = db.Column(db.String(255), nullable=False)

    # FK references
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=True)
    employer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    category = db.Column(db.String(120), nullable=True)
    internship_type = db.Column(db.String(100), nullable=True)

    mode = db.Column(db.String(40), nullable=True)      # On-site / Remote / Hybrid
    location = db.Column(db.String(150), nullable=True)
    duration = db.Column(db.String(80), nullable=True)

    # -----------------------------
    # COMPENSATION
    # -----------------------------
    stipend = db.Column(db.String(80), nullable=True)
    is_paid = db.Column(db.Boolean, default=False)

    # -----------------------------
    # SKILLS & RESPONSIBILITIES
    # -----------------------------
    # Stored as plain TEXT (comma or newline separated)
    skills = db.Column(db.Text, nullable=True)
    responsibilities = db.Column(db.Text, nullable=True)
    tags = db.Column(db.Text, nullable=True)
    company_info = db.Column(db.Text, nullable=True)
    faqs = db.Column(db.Text, nullable=True)

    # -----------------------------
    # ENROLLMENT SYSTEM
    # -----------------------------
    seats = db.Column(db.Integer, default=50)
    enrolled_students = db.Column(db.Text, default="")  # comma-separated user IDs

    # -----------------------------
    # ADMIN VERIFICATION
    # -----------------------------
    status = db.Column(db.String(40), default="Pending")  # Pending / Approved / Rejected

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ----------------------------------------------------
    # HELPERS
    # ----------------------------------------------------
    def enrolled_list(self):
        if not self.enrolled_students:
            return []
        return [int(i) for i in self.enrolled_students.split(",") if i.strip()]

    def seats_left(self):
        return max(self.seats - len(self.enrolled_list()), 0)

    # ----------------------------------------------------
    # DICTIONARY EXPORT
    # ----------------------------------------------------
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company_name": self.company_name,
            "category": self.category,
            "internship_type": self.internship_type,
            "mode": self.mode,
            "location": self.location,
            "duration": self.duration,
            "stipend": self.stipend or "Unpaid",
            "is_paid": self.is_paid,
            "skills": self.skills,
            "responsibilities": self.responsibilities,
            "faqs": self.faqs,
            "seats": self.seats,
            "enrolled_count": len(self.enrolled_list()),
            "seats_left": self.seats_left(),
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d"),
        }

    def __repr__(self):
        return f"<OJT {self.title} ({self.status})>"