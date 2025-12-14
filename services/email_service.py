import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

EMAIL_ADDRESS = "industryconnectcareer@gmail.com"
EMAIL_PASSWORD = "adrj amgt znbi oubn"


# ----------------------------------------------------
# 1️⃣ BASE EMAIL SENDER
# ----------------------------------------------------
def send_email(to, subject, html_content, cc=None, bcc=None):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to

    if cc:
        msg["Cc"] = cc

    recipients = [to] + ([cc] if cc else []) + ([bcc] if bcc else [])

    msg.attach(MIMEText(html_content, "html"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipients, msg.as_string())

        print(f"[EMAIL SENT] → {recipients}")

    except Exception as e:
        print(f"[EMAIL ERROR] {e}")


# ----------------------------------------------------
# 2️⃣ TEMPLATE GENERATOR
# ----------------------------------------------------
def email_template(title, message, button_text=None, button_link=None):

    button_html = ""
    if button_text and button_link:
        button_html = f"""
        <a href='{button_link}'
           style='background:#0a575d;color:white;padding:12px 20px;
                  text-decoration:none;border-radius:6px;display:inline-block;margin-top:15px;'>
            {button_text}
        </a>
        """

    return f"""
    <div style="font-family:Arial;padding:20px;background:#eef2f3;">
        <div style="max-width:600px;margin:auto;background:white;padding:28px;border-radius:12px;">
            <h2 style="color:#0a575d;">{title}</h2>
            <p style="font-size:15px;color:#333;line-height:1.5;">{message}</p>
            {button_html}

            <hr style="margin-top:30px;">
            <p style="font-size:12px;color:gray;text-align:center;">
                Industry Connect Portal • Automated Email
            </p>
        </div>
    </div>
    """


# ----------------------------------------------------
# 3️⃣ OTP EMAIL VERIFICATION (NEW)
# ----------------------------------------------------
def send_email_otp(user_email, otp_code):
    message = f"""
    Please use the OTP below to verify your email address:<br><br>
    <center>
        <div style='font-size:26px;font-weight:bold;color:#0a575d;letter-spacing:3px;'>
            {otp_code}
        </div>
    </center>
    <br>
    This OTP is valid for <b>10 minutes</b>. Do not share it with anyone.
    """

    html = email_template(
        title="🔐 Email Verification OTP",
        message=message,
        button_text="Verify Email",
        button_link="https://your-domain/verify-email"
    )

    send_email(user_email, "Your Email Verification OTP", html)


# ----------------------------------------------------
# 4️⃣ NEW INTERNSHIP NOTIFICATION
# ----------------------------------------------------
def send_new_internship_email(student, internship):

    message = f"""
    A new internship matches your skills:<br><br>
    <b>{internship.title}</b> at <b>{internship.company}</b><br>
    📍 {internship.location} | 💼 {internship.mode}
    """

    html = email_template(
        title="✨ New Internship Recommendation",
        message=message,
        button_text="View Internship",
        button_link=f"https://your-domain/internships/{internship.id}"
    )

    send_email(student.email, "New Internship Available", html)


# ----------------------------------------------------
# 5️⃣ APPLICATION STATUS EMAIL
# ----------------------------------------------------
def send_application_status_email(student, application, status):

    message = f"""
    Your application for <b>{application.internship.title}</b> has been updated.<br><br>
    New Status: <b style='color:#0a575d;'>{status}</b>
    """

    html = email_template(
        title="📄 Application Status Update",
        message=message,
        button_text="View Application",
        button_link=f"https://your-domain/student/applications"
    )

    send_email(student.email, "Application Status Updated", html)


# ----------------------------------------------------
# 6️⃣ OJT ENROLLMENT EMAIL
# ----------------------------------------------------
def send_ojt_enrollment(student, ojt):

    message = f"""
    Congratulations! You are successfully enrolled in:<br><br>
    <b>{ojt.title}</b>
    """

    html = email_template(
        title="🎉 OJT Enrollment Successful",
        message=message,
        button_text="View Program",
        button_link=f"https://your-domain/ojt/{ojt.id}"
    )

    send_email(student.email, "OJT Enrollment Confirmation", html)


# ----------------------------------------------------
# 7️⃣ COMPANY VERIFICATION STATUS
# ----------------------------------------------------
def send_company_status_email(user, company):

    message = f"""
    Your company verification request for:<br>
    <b>{company.company_name}</b><br><br>
    Status: <b>{company.status}</b>
    """

    html = email_template(
        title="🏢 Company Verification Update",
        message=message,
        button_text="View Profile",
        button_link="https://your-domain/employer/company-profile"
    )

    send_email(user.email, "Company Verification Status", html)


# ----------------------------------------------------
# 8️⃣ INTERNSHIP APPROVAL EMAIL
# ----------------------------------------------------
def send_internship_status_email(employer, internship):

    message = f"""
    Your internship posting <b>{internship.title}</b> has been reviewed.<br><br>
    Status: <b>{internship.status}</b>
    """

    html = email_template(
        title="📢 Internship Posting Update",
        message=message,
        button_text="View Posting",
        button_link=f"https://your-domain/employer/postings"
    )

    send_email(employer.email, "Internship Status Update", html)


# ----------------------------------------------------
# 9️⃣ PASSWORD RESET EMAIL
# ----------------------------------------------------
def send_password_reset_email(user, reset_link):

    message = """
    A password reset request was made for your account.<br>
    If this was not you, please ignore this message.
    """

    html = email_template(
        title="🔐 Reset Your Password",
        message=message,
        button_text="Reset Password",
        button_link=reset_link
    )

    send_email(user.email, "Reset Your Password", html)