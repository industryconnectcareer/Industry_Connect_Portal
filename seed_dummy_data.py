import csv
from app import create_app
from extensions import db, bcrypt

from models.user import User
from models.college import College
from models.company import Company
from models.internship import Internship
from models.ojt import OJT
from models.placement import Placement, InternshipMatch

app = create_app()
DATA_DIR = "seed_data"

# ---------------------------------------
# ONE-TIME PASSWORD HASHES
# ---------------------------------------
COLLEGE_HASH = bcrypt.generate_password_hash("College@123").decode()
STUDENT_HASH = bcrypt.generate_password_hash("Student@123").decode()
COMPANY_HASH = bcrypt.generate_password_hash("Company@123").decode()

with app.app_context():

    print("🚀 Seeding dummy data...")

    # ==================================================
    # COLLEGES
    # ==================================================
    with open(f"{DATA_DIR}/colleges.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if User.query.filter_by(email=row["contact_email"]).first():
                continue

            admin = User(
                name=f"{row['name']} Admin",
                email=row["contact_email"],
                password=COLLEGE_HASH,
                role="college",
                is_verified=True
            )
            db.session.add(admin)
            db.session.flush()

            college = College(
                user_id=admin.id,
                name=row["name"],
                contact_email=row["contact_email"],
                university=row["university"],
                accreditation=row["accreditation"],
                website=row["website"],
                status="Approved",
                is_active=True
            )
            db.session.add(college)

    db.session.commit()
    print("✅ Colleges seeded")

    # ==================================================
    # STUDENTS
    # ==================================================
    with open(f"{DATA_DIR}/students_with_skills.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader, start=1):
            if User.query.filter_by(email=row["email"]).first():
                continue

            student = User(
                name=row["name"],
                email=row["email"],
                password=STUDENT_HASH,
                role="student",
                college_id=int(row["college_id"]),
                is_verified=True,
                location=row.get("location"),
                skills=row.get("skills")
            )
            db.session.add(student)

            if i % 500 == 0:
                db.session.commit()
                print(f"✔ {i} students inserted")

    db.session.commit()
    print("✅ Students seeded")

    # ==================================================
    # COMPANIES
    # ==================================================
    with open(f"{DATA_DIR}/companies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if User.query.filter_by(email=row["email"]).first():
                continue

            hr = Employer(
                name=f"{row['company_name']} HR",
                email=row["email"],
                password=COMPANY_HASH,
                role="employer",
                is_verified=True
            )
            db.session.add(hr)
            db.session.flush()

            company = Company(
                user_id=hr.id,
                company_name=row["company_name"],
                tagline=row["tagline"],
                industry=row["industry"],
                location=row["location"],
                address=row["address"],
                website=row["website"],
                contact_number=row["contact_number"],
                contact_email=row["contact_email"],
                company_logo=row["company_logo"],
                banner_image=row["banner_image"],
                status="Approved",
                is_active=True,
                email_verified=True,
                document_verified=True
            )
            db.session.add(company)

    db.session.commit()
    print("✅ Companies seeded")

    company_map = {c.id: c.company_name for c in Company.query.all()}

    # ==================================================
    # INTERNSHIPS
    # ==================================================
    with open(f"{DATA_DIR}/internships_with_skills.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            internship = Internship(
                employer_id=company_user_map[int(row["company_id"])]
                company_id=int(row["company_id"]),
                company_name=company_map.get(int(row["company_id"])),
                title=row["title"],
                mode=row["mode"],
                location=row["location"],
                duration=row["duration"],
                stipend=row["stipend"],
                skills=row["required_skills"],
                responsibilities=row["responsibilities"],
                status="Approved"
            )
            db.session.add(internship)

    db.session.commit()
    print("✅ Internships seeded")

    # ==================================================
    # OJT
    # ==================================================
    with open(f"{DATA_DIR}/ojt.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            ojt = OJT(
                employer_id=company_user_map[int(row["company_id"])]
                company_id=int(row["company_id"]),
                company_name=company_map.get(int(row["company_id"])),
                title=row["title"],
                mode=row["mode"],
                location=row["location"],
                duration=row["duration"],
                stipend=row["stipend"],
                skills=row["required_skills"],
                responsibilities=row["responsibilities"],
                status="Approved"
            )
            db.session.add(ojt)

    db.session.commit()
    print("✅ OJT seeded")

    # ==================================================
    # INTERNSHIP ↔ STUDENT MATCH (ANALYTICS)
    # ==================================================
    with open(f"{DATA_DIR}/internship_student_match.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader, start=1):

            student = db.session.get(User, int(row["student_id"]))
            if not student:
                continue

            match = InternshipMatch(
                internship_id=int(row["internship_id"]),
                student_id=int(row["student_id"]),
                match_score=int(row["match_score"])
            )
            db.session.add(match)

            if i % 1000 == 0:
                db.session.commit()
                print(f"✔ {i} internship matches inserted")

    db.session.commit()
    print("✅ Internship ↔ Student matches seeded")

    # ==================================================
    # FINAL PLACEMENTS (OUTCOME)
    # ==================================================
    with open(f"{DATA_DIR}/placements.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader, start=1):

            placement = Placement(
                student_id=int(row["student_id"]),
                college_id=int(row["college_id"]),
                department_id=int(row["department_id"]),
                academic_year=row["academic_year"],
                company=row["company"],
                role=row.get("role"),
                package=float(row["package"]) if row.get("package") else None,
                is_active=True
            )
            db.session.add(placement)

            if i % 500 == 0:
                db.session.commit()
                print(f"✔ {i} placements inserted")

    db.session.commit()
    print("🎉 ALL DUMMY DATA INSERTED SUCCESSFULLY!")
