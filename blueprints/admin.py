from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db

from models.user import User
from models.company import Company
from models.college import College
from models.internship import Internship
from models.ojt import OJT
from models.applications import Application

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ======================================================
# ADMIN DASHBOARD
# ======================================================
@admin_bp.route("/dashboard")
@login_required
def dashboard():

    # -----------------------------
    # STUDENTS
    # -----------------------------
    total_students = User.query.filter_by(role="student").count()
    pending_students = User.query.filter_by(
        role="student",
        is_verified=False
    ).count()

    # -----------------------------
    # EMPLOYERS / COMPANIES
    # -----------------------------
    total_employers = User.query.filter_by(role="employer").count()
    pending_employers = Company.query.filter_by(status="Pending").count()

    # -----------------------------
    # COLLEGES
    # -----------------------------
    total_colleges = College.query.count()
    pending_colleges = College.query.filter_by(status="Pending").count()

    # -----------------------------
    # INTERNSHIPS
    # -----------------------------
    total_internships = Internship.query.count()
    pending_postings = Internship.query.filter_by(status="Pending").count()

    # -----------------------------
    # OJT PROGRAMS (NEW)
    # -----------------------------
    total_ojts = OJT.query.count()
    pending_ojts = OJT.query.filter_by(status="Pending").count()

    # -----------------------------
    # APPLICATIONS
    # -----------------------------
    total_applications = Application.query.count()
    shortlisted = Application.query.filter_by(status="Shortlisted").count()

    return render_template(
        "admin/dashboard.html",

        # Students
        total_students=total_students,
        pending_students=pending_students,

        # Employers
        total_employers=total_employers,
        pending_employers=pending_employers,

        # Colleges
        total_colleges=total_colleges,
        pending_colleges=pending_colleges,

        # Internships
        total_internships=total_internships,
        pending_postings=pending_postings,

        # OJT
        total_ojts=total_ojts,
        pending_ojts=pending_ojts,

        # Applications
        total_applications=total_applications,
        shortlisted=shortlisted
    )


# ======================================================
# STUDENT VERIFICATION
# ======================================================
@admin_bp.route("/students/pending")
@login_required
def pending_students_list():
    students = User.query.filter_by(
        role="student",
        is_verified=False
    ).all()
    return render_template("admin/pending_students.html", students=students)


@admin_bp.route("/student/<int:user_id>/approve", methods=["POST"])
@login_required
def approve_student(user_id):
    student = User.query.get_or_404(user_id)
    student.is_verified = True
    db.session.commit()

    flash("Student approved successfully!", "success")
    return redirect(url_for("admin.pending_students_list"))


@admin_bp.route("/student/<int:user_id>/reject", methods=["POST"])
@login_required
def reject_student(user_id):
    student = User.query.get_or_404(user_id)
    db.session.delete(student)
    db.session.commit()

    flash("Student rejected and removed.", "danger")
    return redirect(url_for("admin.pending_students_list"))


# ======================================================
# COMPANY VERIFICATION
# ======================================================
@admin_bp.route("/pending-companies")
@login_required
def pending_companies():
    companies = Company.query.filter_by(status="Pending").all()
    return render_template("admin/pending_companies.html", companies=companies)


@admin_bp.route("/company/<int:company_id>/approve", methods=["POST"])
@login_required
def approve_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.status = "Approved"
    db.session.commit()

    flash("Company approved successfully!", "success")
    return redirect(url_for("admin.pending_companies"))


@admin_bp.route("/company/<int:company_id>/reject", methods=["POST"])
@login_required
def reject_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.status = "Rejected"
    db.session.commit()

    flash("Company rejected.", "danger")
    return redirect(url_for("admin.pending_companies"))


# ======================================================
# COLLEGE VERIFICATION
# ======================================================
@admin_bp.route("/pending-colleges")
@login_required
def pending_colleges():
    colleges = College.query.filter_by(status="Pending").all()
    return render_template("admin/pending_colleges.html", colleges=colleges)


@admin_bp.route("/college/<int:college_id>/approve", methods=["POST"])
@login_required
def approve_college(college_id):
    college = College.query.get_or_404(college_id)
    college.status = "Approved"
    college.is_active = True
    db.session.commit()

    flash("College approved successfully!", "success")
    return redirect(url_for("admin.pending_colleges"))


@admin_bp.route("/college/<int:college_id>/reject", methods=["POST"])
@login_required
def reject_college(college_id):
    college = College.query.get_or_404(college_id)
    college.status = "Rejected"
    db.session.commit()

    flash("College rejected.", "danger")
    return redirect(url_for("admin.pending_colleges"))


# ======================================================
# INTERNSHIP VERIFICATION
# ======================================================
@admin_bp.route("/verify-postings")
@login_required
def verify_postings():
    postings = Internship.query.filter_by(status="Pending").all()
    return render_template("admin/verify_postings.html", postings=postings)


@admin_bp.route("/posting/<int:post_id>/approve", methods=["POST"])
@login_required
def approve_posting(post_id):
    post = Internship.query.get_or_404(post_id)
    post.status = "Approved"
    db.session.commit()

    flash("Internship approved!", "success")
    return redirect(url_for("admin.verify_postings"))


@admin_bp.route("/posting/<int:post_id>/reject", methods=["POST"])
@login_required
def reject_posting(post_id):
    post = Internship.query.get_or_404(post_id)
    post.status = "Rejected"
    db.session.commit()

    flash("Internship rejected.", "danger")
    return redirect(url_for("admin.verify_postings"))


# ======================================================
# OJT VERIFICATION (NEW)
# ======================================================
@admin_bp.route("/verify-ojts")
@login_required
def verify_ojts():
    ojts = OJT.query.filter_by(status="Pending").all()
    return render_template("admin/verify_ojts.html", ojts=ojts)


@admin_bp.route("/ojt/<int:ojt_id>/approve", methods=["POST"])
@login_required
def approve_ojt(ojt_id):
    ojt = OJT.query.get_or_404(ojt_id)
    ojt.status = "Approved"
    db.session.commit()

    flash("OJT program approved!", "success")
    return redirect(url_for("admin.verify_ojts"))


@admin_bp.route("/ojt/<int:ojt_id>/reject", methods=["POST"])
@login_required
def reject_ojt(ojt_id):
    ojt = OJT.query.get_or_404(ojt_id)
    ojt.status = "Rejected"
    db.session.commit()

    flash("OJT program rejected.", "danger")
    return redirect(url_for("admin.verify_ojts"))


# ======================================================
# APPLICATIONS OVERVIEW
# ======================================================
@admin_bp.route("/applications")
@login_required
def applications_list():
    applications = Application.query.all()
    return render_template(
        "admin/applications_list.html",
        applications=applications
    )