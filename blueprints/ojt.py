from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.ojt import OJT
from models.saved_item import SavedItem
from ai.recommender import recommend_ojts  # OPTIONAL
from slugify import slugify
import json

ojt_bp = Blueprint("ojt", __name__, url_prefix="/ojt")


# -------------------------------------------------
# OJT LIST PAGE (Filters + Sorting)
# -------------------------------------------------
@ojt_bp.route("/")
def ojt_list():

    category = request.args.get("category")
    mode = request.args.get("mode")
    query = request.args.get("q")
    duration = request.args.get("duration")
    price = request.args.get("price")      # free / paid
    sort_by = request.args.get("sort", "latest")

    ojts = OJT.query.filter_by(status="Approved")

    # -------- Filters --------
    if category:
        ojts = ojts.filter_by(category=category)

    if mode:
        ojts = ojts.filter_by(mode=mode)

    if duration:
        ojts = ojts.filter_by(duration=duration)

    if query:
        ojts = ojts.filter(
            (OJT.title.ilike(f"%{query}%")) |
            (OJT.skills.ilike(f"%{query}%")) |
            (OJT.company_name.ilike(f"%{query}%"))
        )

    if price == "free":
        ojts = ojts.filter(OJT.is_paid == False)
    elif price == "paid":
        ojts = ojts.filter(OJT.is_paid == True)

    # -------- Sorting --------
    if sort_by == "latest":
        ojts = ojts.order_by(OJT.created_at.desc())
    elif sort_by == "popular":
        ojts = ojts.order_by(OJT.seats.asc())  # fewer seats = more popular

    ojt_list = ojts.all()

    # -------- AI Recommendations (optional) --------
    recommended = []
    if current_user.is_authenticated and hasattr(current_user, "skills"):
        recommended = recommend_ojts(current_user.skills)

    return render_template(
        "ojt/ojt_list.html",
        ojt_list=ojt_list,
        recommended=recommended,
        selected_category=category,
        selected_mode=mode,
        selected_duration=duration,
        selected_price=price,
        selected_sort=sort_by,
        query=query
    )


# -------------------------------------------------
# OJT DETAILS PAGE
# -------------------------------------------------
@ojt_bp.route("/<int:ojt_id>")
def ojt_detail(ojt_id):

    program = OJT.query.get_or_404(ojt_id)

    if program.status != "Approved":
        flash("This OJT program is not approved yet.", "warning")
        return redirect(url_for("ojt.ojt_list"))

    is_saved = False
    is_enrolled = False

    if current_user.is_authenticated:
        is_saved = SavedItem.query.filter_by(
            user_id=current_user.id,
            item_type="ojt",
            item_id=ojt_id
        ).first() is not None

        is_enrolled = current_user.id in program.enrolled_list()

    return render_template(
        "ojt/ojt_detail.html",
        program=program,
        is_saved=is_saved,
        is_enrolled=is_enrolled
    )


# -------------------------------------------------
# ADD OJT (Employer / Admin)
# -------------------------------------------------
@ojt_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_ojt():

    if request.method == "POST":

        skills = [
            s.strip()
            for s in request.form.get("skills", "").split(",")
            if s.strip()
        ]

        responsibilities = [
            r.strip()
            for r in request.form.get("responsibilities", "").splitlines()
            if r.strip()
        ]

        ojt = OJT(
            title=request.form["title"],
            slug=slugify(request.form["title"]),
            company_name=request.form["company_name"],
            category=request.form.get("category"),
            mode=request.form.get("mode"),
            location=request.form.get("location"),
            duration=request.form.get("duration"),
            stipend=request.form.get("stipend"),
            is_paid=request.form.get("is_paid") == "true",
            skills=json.dumps(skills),
            responsibilities=json.dumps(responsibilities),
            seats=int(request.form.get("seats", 50)),
            employer_id=current_user.id,
            status="Pending"
        )

        db.session.add(ojt)
        db.session.commit()

        flash("OJT submitted for approval.", "success")
        return redirect(url_for("ojt.ojt_list"))

    return render_template("ojt/add_ojt.html")


# -------------------------------------------------
# ENROLL INTO OJT
# -------------------------------------------------
@ojt_bp.route("/<int:ojt_id>/enroll", methods=["POST"])
@login_required
def ojt_enroll(ojt_id):

    program = OJT.query.get_or_404(ojt_id)
    enrolled = program.enrolled_list()

    if current_user.id in enrolled:
        flash("You are already enrolled.", "info")
        return redirect(url_for("ojt.ojt_detail", ojt_id=ojt_id))

    if program.seats_left() <= 0:
        flash("No seats available.", "danger")
        return redirect(url_for("ojt.ojt_detail", ojt_id=ojt_id))

    enrolled.append(current_user.id)
    program.enrolled_students = json.dumps(enrolled)

    db.session.commit()

    flash("You have successfully enrolled!", "success")
    return redirect(url_for("ojt.ojt_detail", ojt_id=ojt_id))


# -------------------------------------------------
# SAVE / UNSAVE OJT
# -------------------------------------------------
@ojt_bp.route("/<int:ojt_id>/save")
@login_required
def save_ojt(ojt_id):

    existing = SavedItem.query.filter_by(
        user_id=current_user.id,
        item_type="ojt",
        item_id=ojt_id
    ).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash("Removed from saved programs.", "info")
        return redirect(url_for("ojt.ojt_detail", ojt_id=ojt_id))

    saved = SavedItem(
        user_id=current_user.id,
        item_type="ojt",
        item_id=ojt_id
    )

    db.session.add(saved)
    db.session.commit()

    flash("OJT program saved!", "success")
    return redirect(url_for("ojt.ojt_detail", ojt_id=ojt_id))
    