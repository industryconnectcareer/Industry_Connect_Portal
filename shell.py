from models.internship import Internship
from flask_login import current_user

Internship.query.filter_by(employer_id=1).count()
