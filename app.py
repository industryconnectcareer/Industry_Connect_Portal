# ---------------------------------------------
# Industry Connect Portal – Application Factory
# ---------------------------------------------

from flask import Flask, render_template
import logging
import os

from config import Config, ensure_instance_folder
from extensions import db, login_manager, mail, bcrypt


# =====================================================
# APPLICATION FACTORY
# =====================================================
def create_app():
    """Application Factory for Industry Connect Portal"""

    # Ensure instance folder (DB, logs)
    ensure_instance_folder()

    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder="static",
        template_folder="templates"
    )

    # Load config
    app.config.from_object(Config)

    # -------------------------------------------------
    # Initialize Extensions
    # -------------------------------------------------
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # -------------------------------------------------
    # Flask-Login: User Loader
    # -------------------------------------------------
    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # -------------------------------------------------
    # IMPORT ALL MODELS (ORDER MATTERS)
    # -------------------------------------------------
    with app.app_context():
        from models import (
            user,
            company,
            college,
            department,
            internship,
            ojt,
            applications,
            placement,
            readiness_score,
            saved_search,
            saved_item,
            resume_score,
            skill_progress,
            interview_question,
            career_paths,
            skill_gap,
        )

        # ⚠️ Use create_all ONLY in development
        db.create_all()
        create_default_admin()

    # -------------------------------------------------
    # Register Blueprints
    # -------------------------------------------------
    register_blueprints(app)

    # -------------------------------------------------
    # Error Handlers
    # -------------------------------------------------
    register_error_handlers(app)

    # -------------------------------------------------
    # Logging
    # -------------------------------------------------
    configure_logging(app)

    return app


# =====================================================
# BLUEPRINT REGISTRATION
# =====================================================
def register_blueprints(app):

    from blueprints.public import public_bp
    from blueprints.auth import auth_bp
    from blueprints.student import student_bp
    from blueprints.employer import employer_bp
    from blueprints.admin import admin_bp
    from blueprints.college import college_bp
    from blueprints.ojt import ojt_bp
    from blueprints.internships import internships_bp
    from blueprints.resources import resources_bp
    from blueprints.career import career_bp
    from blueprints.mock_interview import mock_bp
    from blueprints.analytics import analytics_bp

    blueprints = [
        public_bp,
        auth_bp,
        student_bp,
        employer_bp,
        admin_bp,
        college_bp,
        ojt_bp,
        internships_bp,
        resources_bp,
        career_bp,
        mock_bp,
        analytics_bp,
    ]

    for bp in blueprints:
        app.register_blueprint(bp)


# =====================================================
# ERROR HANDLERS
# =====================================================
def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.exception("Internal Server Error")
        return render_template("errors/500.html"), 500


# =====================================================
# DEFAULT ADMIN CREATION
# =====================================================
def create_default_admin():
    """Creates default admin if not exists"""

    from models.user import User

    admin_email = "industryconnectcareer@gmail.com"
    admin_password = "Admin@2025"

    existing = User.query.filter_by(email=admin_email).first()
    if existing:
        return

    hashed_pw = bcrypt.generate_password_hash(admin_password).decode("utf-8")

    admin = User(
        name="Industry Connect Admin",
        email=admin_email,
        password=hashed_pw,
        role="admin",
        is_verified=True
    )

    db.session.add(admin)
    db.session.commit()

    print("✔ Default admin created")
    print(f"   Email: {admin_email}")
    print(f"   Password: {admin_password}")


# =====================================================
# LOGGING CONFIG
# =====================================================
def configure_logging(app):

    log_dir = app.instance_path
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, "app.log")

    handler = logging.FileHandler(log_path)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Industry Connect Portal started")

app = create_app()
# =====================================================
# RUN APP (DEV ONLY)
# =====================================================
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
