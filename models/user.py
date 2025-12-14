from datetime import datetime
from flask_login import UserMixin
from extensions import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # ---------------------------------------------------------
    # Basic identity
    # ---------------------------------------------------------
    name = db.Column(db.String(180), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)

    role = db.Column(db.String(30), nullable=False, default="student")
    # student / employer / admin / college

    # ---------------------------------------------------------
    # Academic profile
    # ---------------------------------------------------------
    course = db.Column(db.String(120), nullable=True)
    skills = db.Column(db.Text, nullable=True)      # CSV or free text
    tools = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(120), nullable=True)

    # ---------------------------------------------------------
    # Additional profile
    # ---------------------------------------------------------
    bio = db.Column(db.Text, nullable=True)
    linkedin = db.Column(db.String(255), nullable=True)

    # ---------------------------------------------------------
    # Contact details
    # ---------------------------------------------------------
    mobile = db.Column(db.String(20), nullable=True)
    email_verified = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)

    # ---------------------------------------------------------
    # Resume
    # ---------------------------------------------------------
    resume_path = db.Column(db.String(300), nullable=True)

    # ---------------------------------------------------------
    # College & Academic Structure (NEW – SAFE ADDITIONS)
    # ---------------------------------------------------------
    college_id = db.Column(
        db.Integer,
        db.ForeignKey("colleges.id"),
        nullable=True
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=True
    )

    academic_year = db.Column(
        db.String(20),   # FY / SY / TY / PART1 / PART2
        nullable=True
    )

    # ---------------------------------------------------------
    # System meta
    # ---------------------------------------------------------
    is_active = db.Column(db.Boolean, default=True)    # Soft delete support
    last_login_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    applications = db.relationship("Application", backref="applicant", lazy="dynamic")

    internships = db.relationship(
        "Internship",
        backref="employer",
        lazy="dynamic",
        foreign_keys="Internship.employer_id"
    )

    resume_score = db.relationship("ResumeScore", backref="user", uselist=False)
    readiness = db.relationship("ReadinessScore", backref="user", uselist=False)

    saved_items = db.relationship("SavedItem", backref="user", lazy="dynamic")
    saved_searches = db.relationship("SavedSearch", backref="user", lazy="dynamic")
    skill_gaps = db.relationship("SkillGap", backref="user", lazy="dynamic")
    recent_views = db.relationship("RecentView", backref="user", lazy="dynamic")

    # Academic relationships
    department = db.relationship("Department", backref="students")

    placements = db.relationship(
        "Placement",
        backref="student",
        lazy="dynamic"
    )

    # ---------------------------------------------------------
    # Helper functions
    # ---------------------------------------------------------
    def profile_completion(self):
        fields = [
            self.name, self.course, self.skills, self.tools,
            self.location, self.bio, self.linkedin
        ]
        filled = sum(1 for f in fields if f)
        return int((filled / len(fields)) * 100)

    def short_name(self):
        return self.name.split(" ")[0] if self.name else "User"

    def __repr__(self):
        return f"<User {self.id} {self.email}>"


# ---------------------------------------------------------
# Flask-Login loader
# ---------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))