# models/college.py
from datetime import datetime
import secrets
from extensions import db
from slugify import slugify


def generate_college_code():
    return "COL-" + secrets.token_hex(3).upper()


class College(db.Model):
    __tablename__ = "colleges"

    id = db.Column(db.Integer, primary_key=True)

    # 🔗 College Admin User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)

    # -----------------------------
    # Basic Info
    # -----------------------------
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True)

    college_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        default=generate_college_code
    )

    website = db.Column(db.String(255))
    logo = db.Column(db.String(300))

    # -----------------------------
    # Contact
    # -----------------------------
    contact_email = db.Column(db.String(180), nullable=False)

    university = db.Column(db.String(200))
    accreditation = db.Column(db.String(50))

    # -----------------------------
    # Status
    # -----------------------------
    status = db.Column(db.String(50), default="Pending")
    is_active = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # -----------------------------
    # Relationships (🔥 FIX)
    # -----------------------------
    students = db.relationship(
        "User",
        backref="college",
        foreign_keys="User.college_id",
        lazy=True
    )

    admin_user = db.relationship(
        "User",
        foreign_keys=[user_id],
        backref="managed_college",
        uselist=False
    )

    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<College {self.name} | {self.college_code}>"