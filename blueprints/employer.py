from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db, mail
from models.internship import Internship
from models.ojt import OJT
from models.applications import Application
from models.company import Company
from werkzeug.utils import secure_filename
from flask_mail import Message
import os, random

employer_bp = Blueprint("employer", __name__, url_prefix="/employer")

# ---------------------------------------------------
# FILE UPLOAD PATH
# ---------------------------------------------------
UPLOAD_FOLDER = "static/uploads/company_docs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# OTP store (in-memory)
email_otp_store = {}

# ---------------------------------------------------
# EMPLOYER DASHBOARD
# ---------------------------------------------------
@employer_bp.route("/dashboard")
@login_required
def dashboard():

    total_postings = Internship.query.filter_by(employer_id=current_user.id).count()
    total_ojts = OJT.query.filter_by(employer_id=current_user.id).count()

    total_applications = (
        Application.query.join(Internship)
        .filter(Internship.employer_id == current_user.id)
        .count()
    )

    shortlisted = (
        Application.query.filter_by(status="Shortlisted")
        .join(Internship)
        .filter(Internship.employer_id == current_user.id)
        .count()
    )

    return render_template(
        "employer/dashboard.html",
        total_postings=total_postings,
        total_ojts=total_ojts,
        total_applications=total_applications,
        shortlisted=shortlisted,
    )


# ---------------------------------------------------
# POST INTERNSHIP  (Only if approved)
# ---------------------------------------------------
@employer_bp.route("/post", methods=["GET", "POST"])
@login_required
def post_internship():

    company = Company.query.filter_by(user_id=current_user.id).first()

    if not company:
        flash("Please complete your company profile first.", "warning")
        return redirect(url_for("employer.company_profile"))

    if company.status != "Approved":
        flash("Your company must be approved by admin before posting internships.", "danger")
        return redirect(url_for("employer.company_profile"))

    if not company.email_verified:
        flash("Please verify your business email first.", "danger")
        return redirect(url_for("employer.company_profile"))

    if request.method == "POST":
        internship = Internship(
            title=request.form.get("title"),
            company_name=company.company_name,
            category=request.form.get("category"),
            stipend=request.form.get("stipend"),
            mode=request.form.get("mode"),
            location=request.form.get("location"),
            skills=request.form.get("skills"),
            responsibilities=request.form.get("responsibilities"),
            company_info=company.company_name,
            employer_id=current_user.id,
            status="Pending",
        )

        db.session.add(internship)
        db.session.commit()

        flash("Internship submitted for admin approval!", "success")
        return redirect(url_for("employer.view_postings"))

    return render_template("employer/post_internship.html", company=company)


# ---------------------------------------------------
# VIEW POSTINGS (Internship + OJT)
# ---------------------------------------------------
@employer_bp.route("/postings")
@login_required
def view_postings():

    postings = Internship.query.filter_by(employer_id=current_user.id).all()
    ojts = OJT.query.filter_by(employer_id=current_user.id).all()

    return render_template(
        "employer/view_postings.html",
        postings=postings,
        ojts=ojts
    )


# ---------------------------------------------------
# DELETE INTERNSHIP POSTING
# ---------------------------------------------------
@employer_bp.route("/posting/<int:id>/delete", methods=["POST"])
@login_required
def delete_posting(id):

    internship = Internship.query.get_or_404(id)

    if internship.employer_id != current_user.id:
        flash("Not authorized.", "danger")
        return redirect(url_for("employer.view_postings"))

    Application.query.filter_by(internship_id=id).delete()
    db.session.delete(internship)
    db.session.commit()

    flash("Internship removed successfully!", "success")
    return redirect(url_for("employer.view_postings"))


# ---------------------------------------------------
# APPLICATIONS REVIEW
# ---------------------------------------------------
@employer_bp.route("/applications")
@login_required
def applications_review():

    apps = (
        Application.query.join(Internship)
        .filter(Internship.employer_id == current_user.id)
        .all()
    )

    return render_template("employer/applications_review.html", applications=apps)


@employer_bp.route("/application/<int:id>/shortlist", methods=["POST"])
@login_required
def shortlist_application(id):

    app = Application.query.get_or_404(id)
    app.status = "Shortlisted"
    db.session.commit()

    flash("Applicant shortlisted!", "success")
    return redirect(url_for("employer.applications_review"))


@employer_bp.route("/application/<int:id>/reject", methods=["POST"])
@login_required
def reject_application(id):

    app = Application.query.get_or_404(id)
    app.status = "Rejected"
    db.session.commit()

    flash("Applicant rejected.", "danger")
    return redirect(url_for("employer.applications_review"))


# ---------------------------------------------------
# SEND EMAIL OTP
# ---------------------------------------------------
@employer_bp.route("/send-email-otp", methods=["POST"])
@login_required
def send_email_otp():

    email = request.form.get("email")

    if not email:
        return "invalid"

    otp = str(random.randint(100000, 999999))
    email_otp_store[current_user.id] = otp

    msg = Message(
        "Industry Connect - Email Verification",
        recipients=[email],
    )
    msg.body = f"Your verification OTP is: {otp}"

    try:
        mail.send(msg)
        return "sent"
    except:
        return "error"


# ---------------------------------------------------
# VERIFY EMAIL OTP
# ---------------------------------------------------
@employer_bp.route("/verify-email-otp", methods=["POST"])
@login_required
def verify_email_otp():

    otp = request.form.get("otp")
    stored_otp = email_otp_store.get(current_user.id)

    if otp == stored_otp:
        company = Company.query.filter_by(user_id=current_user.id).first()
        company.email_verified = True
        db.session.commit()
        return "verified"

    return "invalid"


# ---------------------------------------------------
# COMPANY PROFILE SUBMISSION + DOCUMENT UPLOAD
# ---------------------------------------------------
@employer_bp.route("/company-profile", methods=["GET", "POST"])
@login_required
def company_profile():

    company = Company.query.filter_by(user_id=current_user.id).first()

    if request.method == "POST":

        if not company:
            company = Company(user_id=current_user.id, status="Pending")
            db.session.add(company)

        company.company_name = request.form.get("company_name")
        company.description = request.form.get("description")
        company.address = request.form.get("address")
        company.website_url = request.form.get("website_url")
        company.mobile = request.form.get("mobile")
        company.business_email = request.form.get("business_email")

        proof_file = request.files.get("proof_file")
        if proof_file and proof_file.filename:
            filename = secure_filename(proof_file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            proof_file.save(file_path)

            company.proof_document = "/" + file_path.replace("\\", "/")

        # Reset approval if updated
        company.status = "Pending"

        db.session.commit()

        flash("Company profile submitted for admin verification!", "success")
        return redirect(url_for("employer.company_profile"))

    return render_template("employer/company_profile.html", company=company)