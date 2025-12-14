from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from extensions import db, bcrypt

from models.user import User
from models.company import Company
from models.college import College


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# =====================================================
# CONFIG
# =====================================================
ADMIN_SECRET_KEY = "INDUSTRY_ADMIN_2025"
REQUIRE_EMAIL_VERIFICATION = False

ALLOWED_PUBLIC_ROLES = {"student", "employer", "college", "admin"}


# =====================================================
# REGISTER USER
# =====================================================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # -------------------------------
        # FORM DATA
        # -------------------------------
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password")
        role = (request.form.get("role") or "student").strip().lower()
        admin_key = request.form.get("admin_key")
        college_code = (request.form.get("college_code") or "").strip().upper()

        # College-specific fields
        college_name = request.form.get("college_name")
        college_email = request.form.get("college_email")
        university = request.form.get("university")
        accreditation = request.form.get("accreditation")
        website = request.form.get("website")

        # -------------------------------
        # BASIC VALIDATIONS
        # -------------------------------
        if not name or not email or not password:
            flash("❌ All fields are required.", "danger")
            return redirect(url_for("auth.register"))

        if role not in ALLOWED_PUBLIC_ROLES:
            flash("❌ Invalid role selected.", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("⚠ Email already registered.", "warning")
            return redirect(url_for("auth.register"))

        if len(password) < 6:
            flash("❌ Password must be at least 6 characters.", "danger")
            return redirect(url_for("auth.register"))

        # -------------------------------
        # ADMIN VALIDATION
        # -------------------------------
        if role == "admin" and admin_key != ADMIN_SECRET_KEY:
            flash("❌ Invalid Admin Secret Key.", "danger")
            return redirect(url_for("auth.register"))

        # -------------------------------
        # STUDENT → COLLEGE CODE VALIDATION
        # -------------------------------
        college = None
        if role == "student":

            if not college_code:
                flash("❌ College ID is required for students.", "danger")
                return redirect(url_for("auth.register"))

            college = College.query.filter_by(
                college_code=college_code,
                status="Approved",
                is_active=True
            ).first()

            if not college:
                flash("❌ Invalid College ID. Please check with your college.", "danger")
                return redirect(url_for("auth.register"))

        # -------------------------------
        # HASH PASSWORD
        # -------------------------------
        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

        # -------------------------------
        # CREATE USER
        # -------------------------------
        new_user = User(
            name=name,
            email=email,
            password=hashed_pw,
            role=role,
            email_verified=False,
            college_id=college.id if role == "student" else None
        )

        db.session.add(new_user)
        db.session.commit()

        # -------------------------------
        # EMPLOYER → CREATE COMPANY
        # -------------------------------
        if role == "employer":
            company = Company(
                user_id=new_user.id,
                status="Pending"
            )
            db.session.add(company)
            db.session.commit()

        # -------------------------------
        # COLLEGE → CREATE COLLEGE (PENDING)
        # -------------------------------
        if role == "college":

            if not college_name or not college_email:
                flash("❌ College name and official email are required.", "danger")
                return redirect(url_for("auth.register"))

            # Prevent duplicate college
            if College.query.filter_by(contact_email=college_email).first():
                flash("⚠ This college is already registered.", "warning")
                return redirect(url_for("auth.register"))

            college = College(
                name=college_name,
                contact_email=college_email,
                university=university,
                accreditation=accreditation,
                website=website,
                status="Pending",
                is_active=False,
                user_id=new_user.id
            )

            db.session.add(college)
            db.session.commit()

        flash("🎉 Registration successful! Await admin approval.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# =====================================================
# LOGIN USER (SINGLE LOGIN FOR ALL ROLES)
# =====================================================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("❌ Email not found.", "danger")
            return redirect(url_for("auth.login"))

        if not bcrypt.check_password_hash(user.password, password):
            flash("❌ Incorrect password.", "danger")
            return redirect(url_for("auth.login"))

        if REQUIRE_EMAIL_VERIFICATION and not user.email_verified:
            flash("📧 Please verify your email.", "warning")
            return redirect(url_for("auth.login"))

        # -------------------------------
        # LOGIN
        # -------------------------------
        login_user(user)

        # -------------------------------
        # ROLE REDIRECT
        # -------------------------------
        if user.role == "student":
            return redirect(url_for("student.dashboard"))

        if user.role == "employer":
            return redirect(url_for("employer.dashboard"))

        if user.role == "college":
            return redirect(url_for("college.dashboard"))

        if user.role == "admin":
            return redirect(url_for("admin.dashboard"))

        flash("Invalid role configuration.", "danger")
        return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


# =====================================================
# LOGOUT
# =====================================================
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("👋 Logged out successfully.", "info")
    return redirect(url_for("auth.login"))