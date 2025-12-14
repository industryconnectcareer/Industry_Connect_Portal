# models/internship.py
from datetime import datetime
from app import db
from slugify import slugify   # pip install python-slugify


class Internship(db.Model):
    __tablename__ = "internships"

    id = db.Column(db.Integer, primary_key=True)

    # -----------------------------
    # BASIC DETAILS
    # -----------------------------
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True)

    # IMPORTANT FIX
    company_name = db.Column(db.String(255), nullable=False)

    # FK to Company table
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=True)

    employer_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    category = db.Column(db.String(120), nullable=True)
    internship_type = db.Column(db.String(100), nullable=True)

    mode = db.Column(db.String(40), nullable=True)
    location = db.Column(db.String(150), nullable=True)
    duration = db.Column(db.String(80), nullable=True)

    # -----------------------------
    # COMPENSATION
    # -----------------------------
    stipend = db.Column(db.String(80), nullable=True)
    is_paid = db.Column(db.Boolean, default=False)

    # -----------------------------
    # SKILLS & DESCRIPTION
    # -----------------------------
    skills = db.Column(db.Text, nullable=True)
    tags = db.Column(db.Text, nullable=True)
    responsibilities = db.Column(db.Text, nullable=True)
    company_info = db.Column(db.Text, nullable=True)

    # -----------------------------
    # DOCUMENTS / LETTERS
    # -----------------------------
    offer_letter = db.Column(db.String(255), nullable=True)
    completion_certificate = db.Column(db.String(255), nullable=True)

    # -----------------------------
    # ADMIN STATUS
    # -----------------------------
    status = db.Column(db.String(40), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # -----------------------------
    # ANALYTICS
    # -----------------------------
    views = db.Column(db.Integer, default=0)
    applications_count = db.Column(db.Integer, default=0)
    popularity_score = db.Column(db.Float, default=0.0)

    is_active = db.Column(db.Boolean, default=True)

    # -----------------------------
    # RELATIONSHIPS
    # -----------------------------
    applications = db.relationship(
        "Application",
        back_populates="internship",
        cascade="all, delete-orphan"
    )

    # -----------------------------
    # HELPERS
    # -----------------------------
    def skill_list(self):
        return [s.strip() for s in (self.skills or "").split(",") if s.strip()]

    def tag_list(self):
        return [t.strip() for t in (self.tags or "").split(",") if t.strip()]

    def generate_slug(self):
        if not self.slug:
            base = f"{self.title}-{self.company_name}"
            self.slug = slugify(base)

    def update_popularity(self):
        self.popularity_score = (self.views * 0.2) + (self.applications_count * 1.5)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "company": self.company_name,
            "company_id": self.company_id,
            "employer_id": self.employer_id,
            "category": self.category,
            "internship_type": self.internship_type,
            "stipend": self.stipend,
            "is_paid": self.is_paid,
            "mode": self.mode,
            "location": self.location,
            "duration": self.duration,
            "skills": self.skill_list(),
            "tags": self.tag_list(),
            "responsibilities": self.responsibilities,
            "company_info": self.company_info,
            "offer_letter": self.offer_letter,
            "completion_certificate": self.completion_certificate,
            "status": self.status,
            "views": self.views,
            "applications_count": self.applications_count,
            "popularity_score": round(self.popularity_score, 2),
            "created_at": self.created_at.strftime("%Y-%m-%d"),
        }

    def save(self):
        self.generate_slug()
        self.update_popularity()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Internship {self.title} at {self.company_name}>"