# utils/mailer.py

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

EMAIL_ADDRESS = "industryconnectcareer@gmail.com"
EMAIL_PASSWORD = "adrj amgt znbi oubn"

# Folder that contains all your HTML email templates
TEMPLATE_DIR = "emails"


# -------------------------------------------------------
# Load HTML Email Template + Inject Dynamic Variables
# -------------------------------------------------------
def load_template(template_name, **kwargs):
    """
    Loads an HTML file and replaces {{ variables }} with provided values.
    """
    path = os.path.join(TEMPLATE_DIR, template_name)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Template not found: {path}")

    with open(path, "r", encoding="utf-8") as file:
        html = file.read()

    # Replace {{ variable }} inside the template
    for key, value in kwargs.items():
        html = html.replace(f"{{{{ {key} }}}}", str(value))

    return html


# -------------------------------------------------------
# Send Single Email (with optional attachment)
# -------------------------------------------------------
def send_email(to, subject, html_content, attachment_path=None):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to

    msg.attach(MIMEText(html_content, "html"))

    # Optional attachment
    if attachment_path:
        with open(attachment_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)

    # SMTP Server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to, msg.as_string())

    print(f"✓ Email sent → {to}")


# -------------------------------------------------------
# Bulk Email Sender
# -------------------------------------------------------
def send_bulk_emails(receivers, subject, template_name, attachment=None, **template_vars):
    """
    receivers      → list of {"email": "...", "name": "..."} dictionaries
    subject        → subject of email
    template_name  → HTML filename inside emails/ folder
    attachment     → optional attachment
    template_vars  → additional values injected into template
    """

    results = {"sent": [], "failed": []}

    for user in receivers:
        try:
            html = load_template(template_name, **template_vars, **user)
            send_email(user["email"], subject, html, attachment)
            results["sent"].append(user["email"])

        except Exception as e:
            print(f"❌ Error sending to {user['email']}: {e}")
            results["failed"].append({"email": user["email"], "error": str(e)})

    return results