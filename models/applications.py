# models/applications.py
from datetime import datetime
from app import db


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    internship_id = db.Column(
        db.Integer,
        db.ForeignKey("internships.id"),
        nullable=False,
        index=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # ✅ RELATIONSHIP → Internship (THIS FIXES YOUR TEMPLATE)
    internship = db.relationship(
        "Internship",
        back_populates="applications",
        lazy=True
    )

    cover_letter = db.Column(db.Text, nullable=True)
    resume_path = db.Column(db.String(300), nullable=True)

    # -----------------------------
    # STATUS WORKFLOW
    # -----------------------------
    status = db.Column(
        db.String(40),
        default="Applied",
        index=True
    )

    # -----------------------------
    # TIMESTAMPS
    # -----------------------------
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Required for sorting & dashboards
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # -----------------------------
    # SOFT DELETE
    # -----------------------------
    is_active = db.Column(db.Boolean, default=True)

    # -----------------------------
    # PREVENT DUPLICATE APPLICATIONS
    # -----------------------------
    __table_args__ = (
        db.UniqueConstraint(
            "internship_id",
            "user_id",
            name="unique_student_application"
        ),
    )

    # -------------------------------
    # STATUS UPDATE HELPER
    # -------------------------------
    def update_status(self, new_status):
        from models.application_history import ApplicationHistory

        old_status = self.status
        self.status = new_status
        self.updated_at = datetime.utcnow()

        history = ApplicationHistory(
            application_id=self.id,
            old_status=old_status,
            new_status=new_status
        )
        db.session.add(history)

    # -------------------------------
    # STATUS BADGE COLOR
    # -------------------------------
    def status_color(self):
        return {
            "Applied": "blue",
            "Under Review": "purple",
            "Shortlisted": "orange",
            "Selected": "green",
            "Rejected": "red",
        }.get(self.status, "gray")

    # -------------------------------
    # REPRESENTATION
    # -------------------------------
    def __repr__(self):
        return (
            f"<Application user:{self.user_id} | "
            f"internship:{self.internship_id} | "
            f"status:{self.status}>"
        )