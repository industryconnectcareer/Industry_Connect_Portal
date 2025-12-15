from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db, bcrypt, mail
from flask_mail import Message
from sqlalchemy import func
import csv, secrets, string

from models.college import College
from models.user import User
from models.department import Department
from models.placement import Placement


college_bp = Blueprint("college", __name__, url_prefix="/college")


# =====================================================
# ACCESS CHECK
# =====================================================
def get_college_or_redirect():
    if current_user.role != "college":
        flash("Unauthorized access", "danger")
        return None

    college = College.query.filter_by(
        user_id=current_user.id
    ).first()

    if not college:
        flash("College profile not found", "danger")
        return None

    if college.status != "Approved":
        flash("College account not approved yet", "warning")
        return None

    if not college.is_active:
        flash("College account is inactive", "danger")
        return None

    return college



# =====================================================
# DASHBOARD
# =====================================================
@college_bp.route("/dashboard")
@login_required
def dashboard():
    college = get_college_or_redirect()
    if not college:
        return redirect(url_for("auth.login"))

    students = User.query.filter_by(college_id=college.id).all()

    total_students = len(students)
    verified_students = User.query.filter_by(
        college_id=college.id,
        is_verified=True
    ).count()

    placed_students = Placement.query.filter_by(
        college_id=college.id
    ).count()

    placement_percent = (
        round((placed_students / total_students) * 100, 2)
        if total_students else 0
    )

    return render_template(
        "college/dashboard.html",
        college=college,
        students=students,
        total_students=total_students,
        verified_students=verified_students,
        placement_percent=placement_percent
    )

# =====================================================
# STUDENTS LIST
# =====================================================
@college_bp.route("/students")
@login_required
def students():
    college = get_college_or_redirect()
    if not college:
        return redirect(url_for("auth.login"))

    students = User.query.filter_by(college_id=college.id).all()

    return render_template(
        "college/students.html",
        college=college,
        students=students
    )

# =====================================================
# PLACEMENT ANALYTICS
# =====================================================
@college_bp.route("/analytics")
@login_required
def analytics():
    college = get_college_or_redirect()
    if not college:
        return redirect(url_for("auth.login"))

    # Year-wise placements
    year_data = (
        db.session.query(
            Placement.academic_year,
            func.count(Placement.id)
        )
        .filter(Placement.college_id == college.id)
        .group_by(Placement.academic_year)
        .all()
    )

    years = [y[0] for y in year_data]
    year_counts = [y[1] for y in year_data]

    # Department-wise placements
    dept_data = (
        db.session.query(
            Department.name,
            func.count(Placement.id)
        )
        .join(Placement, Placement.department_id == Department.id)
        .filter(Placement.college_id == college.id)
        .group_by(Department.name)
        .all()
    )

    departments = [d[0] for d in dept_data]
    dept_counts = [d[1] for d in dept_data]

    return render_template(
        "college/analytics.html",
        years=years,
        year_counts=year_counts,
        departments=departments,
        dept_counts=dept_counts
    )


# =====================================================
# BULK IMPORT STUDENTS
# =====================================================
@college_bp.route("/import", methods=["GET", "POST"])
@login_required
def import_students():
    college = get_college_or_redirect()
    if not college:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        file = request.files.get("file")

        if not file or not file.filename.endswith(".csv"):
            flash("Upload a valid CSV file", "danger")
            return redirect(url_for("college.import_students"))

        reader = csv.DictReader(file.stream.read().decode("utf-8").splitlines())

        imported, skipped = 0, 0

        for row in reader:
            if not row.get("email") or not row.get("name"):
                skipped += 1
                continue

            if User.query.filter_by(email=row["email"]).first():
                skipped += 1
                continue

            password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
            hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

            student = User(
                name=row["name"].strip(),
                email=row["email"].strip(),
                password=hashed_pw,
                role="student",
                college_id=college.id,
                is_verified=True
            )

            db.session.add(student)
            imported += 1

            try:
                msg = Message(
                    "Your Student Account – Industry Connect",
                    recipients=[student.email]
                )
                msg.body = f"""
Hello {student.name},

Your account has been created.

Email: {student.email}
Password: {password}

Please login and change your password.
"""
                mail.send(msg)
            except Exception:
                pass

        db.session.commit()

        flash(f"{imported} students imported", "success")
        if skipped:
            flash(f"{skipped} rows skipped", "warning")

        return redirect(url_for("college.dashboard"))

    return render_template("college/import_students.html")
