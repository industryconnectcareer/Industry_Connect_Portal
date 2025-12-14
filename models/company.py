# models/company.py
from datetime import datetime
from app import db
from slugify import slugify   # pip install python-slugify


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)

    # -------------------------------------------------
    # LINKED EMPLOYER ACCOUNT
    # -------------------------------------------------
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # -------------------------------------------------
    # BASIC COMPANY INFO
    # -------------------------------------------------
    company_name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True)
    tagline = db.Column(db.String(255), nullable=True)
    industry = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(300), nullable=True)
    contact_number = db.Column(db.String(20), nullable=True)
    contact_email = db.Column(db.String(180), nullable=True)

    # -------------------------------------------------
    # BRANDING
    # -------------------------------------------------
    company_logo = db.Column(db.String(255), nullable=True)
    banner_image = db.Column(db.String(255), nullable=True)

    # -------------------------------------------------
    # VERIFICATION FLAGS
    # -------------------------------------------------
    email_verified = db.Column(db.Boolean, default=False)
    document_verified = db.Column(db.Boolean, default=False)

    # -------------------------------------------------
    # ADMIN STATUS
    # -------------------------------------------------
    status = db.Column(
        db.String(40),
        default="Pending"   # Pending / Approved / Rejected
    )

    is_active = db.Column(db.Boolean, default=True)

    # -------------------------------------------------
    # META INFO
    # -------------------------------------------------
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # -------------------------------------------------
    # RELATIONSHIPS
    # -------------------------------------------------
    employer = db.relationship(
        "User",
        backref=db.backref("company_profile", uselist=False),
        lazy=True
    )

    internships = db.relationship(
        "Internship",
        backref="company_ref",
        lazy=True,
        foreign_keys="Internship.company_id"
    )

    ojts = db.relationship(
        "OJT",
        backref="company_ref",
        lazy=True,
        foreign_keys="OJT.company_id"
    )

    # -------------------------------------------------
    # DERIVED PROPERTIES
    # -------------------------------------------------
    @property
    def is_verified(self):
        return (
            self.status == "Approved"
            and self.email_verified
            and self.document_verified
        )

    @property
    def profile_completion(self):
        """
        Returns profile completion percentage.
        """
        fields = [
            self.company_name,
            self.address,
            self.website,
            self.contact_number,
            self.company_logo,
            self.banner_image,
        ]
        filled = sum(1 for f in fields if f)
        return int((filled / len(fields)) * 100)

    # -------------------------------------------------
    # SAVE WITH SLUG AUTO-GENERATION
    # -------------------------------------------------
    def save(self):
        if not self.slug:
            self.slug = slugify(self.company_name)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Company {self.company_name} | Status: {self.status}>"