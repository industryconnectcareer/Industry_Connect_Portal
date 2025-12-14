from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.internship import Internship
from models.applications import Application
from models.ojt import OJT
from models.saved_item import SavedItem
from ai.recommender import recommend_internships
from models.recent_view import RecentView   # ✅ NEW: for recently viewed tracking

internships_bp = Blueprint("internships", __name__, url_prefix="/internships")


# ------------------------------------------------------------
# SHOW ALL APPROVED INTERNSHIPS + FILTERS
# ------------------------------------------------------------
@internships_bp.route("/")
def internship_list():
    category = request.args.get("category", "").strip()
    mode = request.args.get("mode", "").strip()
    location = request.args.get("location", "").strip()
    stipend = request.args.get("stipend", "").strip()
    skill = request.args.get("skill", "").strip()

    q = Internship.query.filter_by(status="Approved")

    if category:
        q = q.filter(Internship.category.ilike(f"%{category}%"))

    if mode:
        q = q.filter(Internship.mode.ilike(f"%{mode}%"))

    if location:
        q = q.filter(Internship.location.ilike(f"%{location}%"))

    if stipend:
        q = q.filter(Internship.stipend.ilike(f"%{stipend}%"))

    if skill:
        q = q.filter(Internship.skills.ilike(f"%{skill}%"))

    internships = q.order_by(Internship.id.desc()).all()

    return render_template(
        "internships/internship_list.html",
        internships=internships,
        selected_category=category,
        selected_mode=mode,
        selected_location=location,
        selected_stipend=stipend,
        selected_skill=skill,
    )


# ------------------------------------------------------------
# INTERNSHIP DETAILS PAGE + TRACK RECENT VIEWS
# ------------------------------------------------------------
@internships_bp.route("/<int:id>")
def internship_detail(id):
    internship = Internship.query.get_or_404(id)

    # Prevent unapproved internships being opened
    if internship.status != "Approved":
        flash("This internship is not approved yet.", "warning")
        return redirect(url_for("internships.internship_list"))

    is_owner = False
    has_applied = False
    is_saved = False

    if current_user.is_authenticated:
        is_owner = internship.employer_id == current_user.id

        # Check if applied
        app = Application.query.filter_by(
            internship_id=id, user_id=current_user.id
        ).first()
        has_applied = app is not None

        # Check if saved
        saved = SavedItem.query.filter_by(
            user_id=current_user.id, item_type="internship", item_id=id
        ).first()
        is_saved = saved is not None

        # ----------------------------------------------------
        # ⭐ NEW: Track Recently Viewed Internship
        # ----------------------------------------------------
        # Remove previous views of same internship (avoid duplicates)
        RecentView.query.filter_by(
            user_id=current_user.id,
            internship_id=id
        ).delete()

        # Add new recent view entry
        new_view = RecentView(
            user_id=current_user.id,
            internship_id=id
        )
        db.session.add(new_view)
        db.session.commit()

    return render_template(
        "internships/internship_detail.html",
        internship=internship,
        is_owner=is_owner,
        has_applied=has_applied,
        is_saved=is_saved,
    )


# ------------------------------------------------------------
# APPLY FOR INTERNSHIP
# ------------------------------------------------------------
@internships_bp.route("/<int:id>/apply", methods=["GET", "POST"])
@login_required
def internship_apply(id):
    internship = Internship.query.get_or_404(id)

    if internship.employer_id == current_user.id:
        flash("You cannot apply to your own internship!", "danger")
        return redirect(url_for("internships.internship_detail", id=id))

    already_applied = Application.query.filter_by(
        internship_id=id, user_id=current_user.id
    ).first()

    if already_applied:
        flash("You have already applied to this internship.", "info")
        return redirect(url_for("student.applications"))

    if request.method == "POST":
        new_app = Application(
            internship_id=id,
            user_id=current_user.id,
            status="Applied"
        )
        db.session.add(new_app)
        db.session.commit()

        flash("Application submitted successfully!", "success")
        return redirect(url_for("student.applications"))

    return render_template("internships/internship_apply.html", internship=internship)


# ------------------------------------------------------------
# SAVE / UNSAVE INTERNSHIP
# ------------------------------------------------------------
@internships_bp.route("/<int:id>/save")
@login_required
def save_internship(id):
    internship = Internship.query.get_or_404(id)

    existing = SavedItem.query.filter_by(
        user_id=current_user.id,
        item_type="internship",
        item_id=id
    ).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash("Internship removed from your saved list.", "info")
    else:
        saved = SavedItem(
            user_id=current_user.id,
            item_type="internship",
            item_id=id
        )
        db.session.add(saved)
        db.session.commit()
        flash("Internship saved to your wishlist!", "success")

    return redirect(url_for("internships.internship_detail", id=id))


# ------------------------------------------------------------
# VIEW SAVED / WISHLIST INTERNSHIPS
# ------------------------------------------------------------
@internships_bp.route("/saved")
@login_required
def saved_internships():
    saved_items = SavedItem.query.filter_by(
        user_id=current_user.id,
        item_type="internship"
    ).all()

    saved_ids = [s.item_id for s in saved_items]

    internships = Internship.query.filter(
        Internship.id.in_(saved_ids),
        Internship.status == "Approved"
    ).all()

    return render_template("internships/saved_list.html", internships=internships)


# ------------------------------------------------------------
# CATEGORY FILTER (Internships + OJT)
# ------------------------------------------------------------
@internships_bp.route("/category/<string:category>")
def category_filter(category):
    internships = Internship.query.filter_by(
        category=category, status="Approved"
    ).order_by(Internship.id.desc()).all()

    ojts = OJT.query.filter_by(
        category=category, status="Approved"
    ).order_by(OJT.id.desc()).all()

    return render_template(
        "internships/categories.html",
        internships=internships,
        ojts=ojts,
        selected_category=category
    )


# ------------------------------------------------------------
# SEARCH ENGINE
# ------------------------------------------------------------
@internships_bp.route("/search")
def internship_search():
    query = request.args.get("q", "").strip()

    if query == "":
        return render_template(
            "internships/search_results.html",
            query=query,
            internships=[],
            ojts=[]
        )

    search_filter = (
        (Internship.title.ilike(f"%{query}%")) |
        (Internship.skills.ilike(f"%{query}%")) |
        (Internship.location.ilike(f"%{query}%")) |
        (Internship.category.ilike(f"%{query}%"))
    )

    internships = Internship.query.filter(
        search_filter, Internship.status == "Approved"
    ).all()

    ojts = OJT.query.filter(
        OJT.title.ilike(f"%{query}%"), OJT.status == "Approved"
    ).all()

    return render_template(
        "internships/search_results.html",
        query=query,
        internships=internships,
        ojts=ojts
    )


# ------------------------------------------------------------
# RECOMMENDED INTERNSHIPS FOR STUDENT
# ------------------------------------------------------------
@internships_bp.route("/recommended")
@login_required
def recommended_for_student():
    if current_user.role != "student":
        flash("Recommendations are only available for students.", "warning")
        return redirect(url_for("internships.internship_list"))

    try:
        recommended_list = recommend_internships(current_user)
    except Exception as e:
        print("AI recommend_internships error:", e)
        recommended_list = []

    return render_template("internships/recommended.html", internships=recommended_list)


# ------------------------------------------------------------
# APPLICATION TRACKER
# ------------------------------------------------------------
@internships_bp.route("/my-applications")
@login_required
def my_applications_tracker():
    apps = Application.query.join(Internship).filter(
        Application.user_id == current_user.id
    ).order_by(Application.id.desc()).all()

    status_counts = {
        "Applied": 0,
        "Shortlisted": 0,
        "Rejected": 0,
        "Selected": 0,
    }

    for a in apps:
        if a.status in status_counts:
            status_counts[a.status] += 1

    return render_template(
        "internships/my_applications.html",
        applications=apps,
        status_counts=status_counts
    )


# ------------------------------------------------------------
# INTERNSHIP COMPARISON
# ------------------------------------------------------------
@internships_bp.route("/compare")
def compare_internships():
    ids_param = request.args.get("ids", "").strip()

    if not ids_param:
        flash("Select internships to compare.", "info")
        return redirect(url_for("internships.internship_list"))

    try:
        id_list = [int(x) for x in ids_param.split(",") if x.strip().isdigit()]
    except ValueError:
        id_list = []

    if not id_list:
        flash("Invalid selection for comparison.", "danger")
        return redirect(url_for("internships.internship_list"))

    internships = Internship.query.filter(
        Internship.id.in_(id_list),
        Internship.status == "Approved"
    ).all()

    return render_template("internships/compare.html", internships=internships)