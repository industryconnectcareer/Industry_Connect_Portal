from flask import send_file
from io import BytesIO
from datetime import datetime

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from extensions import db
from models.college import College
from models.department import Department
from models.user import User
from models.placement import Placement


# =====================================================
# EXCEL EXPORT
# =====================================================

def export_excel(college_id):
    college = College.query.get_or_404(college_id)

    placements = (
        db.session.query(
            User.name.label("Student Name"),
            Department.name.label("Department"),
            Placement.academic_year.label("Year"),
            Placement.company.label("Company"),
            Placement.role.label("Role"),
            Placement.package.label("Package (LPA)")
        )
        .join(Placement, Placement.student_id == User.id)
        .join(Department, Placement.department_id == Department.id)
        .filter(Placement.college_id == college_id)
        .all()
    )

    df = pd.DataFrame(placements)

    if df.empty:
        df = pd.DataFrame(
            columns=[
                "Student Name", "Department", "Year",
                "Company", "Role", "Package (LPA)"
            ]
        )

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Placements")

    output.seek(0)

    filename = f"{college.slug or 'college'}_placements_{datetime.now().date()}.xlsx"

    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# =====================================================
# PDF EXPORT
# =====================================================

def export_pdf(college_id):
    college = College.query.get_or_404(college_id)

    placements = (
        db.session.query(
            User.name,
            Department.name,
            Placement.academic_year,
            Placement.company,
            Placement.role,
            Placement.package
        )
        .join(Placement, Placement.student_id == User.id)
        .join(Department, Placement.department_id == Department.id)
        .filter(Placement.college_id == college_id)
        .all()
    )

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(
        Paragraph(
            f"<b>{college.name} – Placement Report</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%d %B %Y')}",
            styles["Normal"]
        )
    )

    elements.append(Paragraph("<br/>", styles["Normal"]))

    # Table data
    table_data = [
        ["Student", "Department", "Year", "Company", "Role", "Package (LPA)"]
    ]

    for p in placements:
        table_data.append([
            p[0],
            p[1],
            p[2],
            p[3],
            p[4] or "",
            p[5] or ""
        ])

    if len(table_data) == 1:
        table_data.append(["-", "-", "-", "-", "-", "-"])

    table = Table(table_data, repeatRows=1)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (2, 1), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
    ]))

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    filename = f"{college.slug or 'college'}_placements_{datetime.now().date()}.pdf"

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )