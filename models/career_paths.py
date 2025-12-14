# models/career_paths.py
import json
import re
from app import db
from slugify import slugify   # pip install python-slugify


class CareerPath(db.Model):
    __tablename__ = "career_paths"

    id = db.Column(db.Integer, primary_key=True)

    # Core career data
    name = db.Column(db.String(180), nullable=False, unique=True)
    slug = db.Column(db.String(200), unique=True)  # SEO-friendly URL

    category = db.Column(db.String(120), nullable=True)  
    # Examples: "Finance", "Accounting", "Taxation", "Banking"

    description = db.Column(db.Text, nullable=True)

    # Skills required (CSV)
    skills = db.Column(db.Text, nullable=True)

    # Industry tags (CSV)
    tags = db.Column(db.Text, nullable=True)
    # Example: "finance, accounting, analysis, taxation"

    # Difficulty level
    difficulty = db.Column(db.String(50), default="Beginner")
    # Beginner / Intermediate / Advanced

    # Career growth roadmap (JSON recommended)
    roadmap = db.Column(db.Text, nullable=True)

    # Salary information (India-based)
    avg_salary = db.Column(db.Integer, nullable=True)  # IN ₹ (Annual)

    # Popularity for ranking/trending
    trending_score = db.Column(db.Integer, default=50)

    # --------------------------
    # LIFECYCLE HOOKS
    # --------------------------
    def save(self):
        """Auto-generate slug & save."""
        if not self.slug:
            self.slug = slugify(self.name)
        db.session.add(self)
        db.session.commit()

    # --------------------------
    # LIST HELPERS
    # --------------------------
    def skills_list(self):
        return [s.strip() for s in (self.skills or "").split(",") if s.strip()]

    def tags_list(self):
        return [t.strip() for t in (self.tags or "").split(",") if t.strip()]

    def roadmap_list(self):
        try:
            data = json.loads(self.roadmap or "[]")
            if isinstance(data, list):
                return data
        except:
            # fallback: newline separated
            return [r.strip() for r in (self.roadmap or "").split("\n") if r.strip()]
        return []

    # --------------------------
    # AI: SKILL MATCHING SCORE
    # --------------------------
    def match_score(self, student_skills: list):
        """Returns match % between student's skills and career path."""
        required = set([s.lower() for s in self.skills_list()])
        student = set([s.lower() for s in student_skills])

        if not required:
            return 0

        matches = required.intersection(student)
        percent = int((len(matches) / len(required)) * 100)
        return percent

    # --------------------------
    # SEARCH HELPER
    # --------------------------
    @staticmethod
    def search(term):
        term = f"%{term.lower()}%"
        return CareerPath.query.filter(
            db.or_(
                db.func.lower(CareerPath.name).like(term),
                db.func.lower(CareerPath.tags).like(term),
                db.func.lower(CareerPath.skills).like(term),
                db.func.lower(CareerPath.category).like(term),
            )
        ).all()

    def __repr__(self):
        return f"<CareerPath {self.name} | {self.category}>"