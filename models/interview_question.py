# models/interview_question.py
from app import db
from datetime import datetime
import json


class InterviewQuestion(db.Model):
    __tablename__ = "interview_questions"

    id = db.Column(db.Integer, primary_key=True)

    # ----------------------------
    # MAIN QUESTION DETAILS
    # ----------------------------
    question = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=True)          # model answer (NEW)

    category = db.Column(db.String(120), nullable=True)      # Finance, Accounting, GST, HR...
    topic = db.Column(db.String(120), nullable=True)         # Sub-topic: Tally, Balance Sheet, GST Input...

    question_type = db.Column(db.String(40), default="theory")  
    # theory / mcq / case / scenario

    difficulty = db.Column(db.String(30), default="medium")
    difficulty_score = db.Column(db.Integer, default=2)       # easy=1, medium=2, hard=3

    # ----------------------------
    # MCQ SUPPORT (Optional)
    # ----------------------------
    options_json = db.Column(db.Text, nullable=True)          # store list as JSON
    correct_answer = db.Column(db.String(10), nullable=True)  # A/B/C/D

    # ----------------------------
    # SEARCH & AI TAGGING
    # ----------------------------
    keywords = db.Column(db.Text, nullable=True)              # auto-generated tags

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ----------------------------
    # HELPERS
    # ----------------------------
    def set_options(self, options_list):
        """Save list of options as JSON."""
        self.options_json = json.dumps(options_list, ensure_ascii=False)

    def get_options(self):
        """Return MCQ options as Python list."""
        try:
            return json.loads(self.options_json or "[]")
        except:
            return []

    def keyword_list(self):
        """Returns keywords split cleanly."""
        return [k.strip() for k in (self.keywords or "").split(",") if k.strip()]

    def to_dict(self):
        """Return AI-ready dictionary."""
        return {
            "id": self.id,
            "question": self.question,
            "explanation": self.explanation,
            "category": self.category,
            "topic": self.topic,
            "question_type": self.question_type,
            "difficulty": self.difficulty,
            "difficulty_score": self.difficulty_score,
            "options": self.get_options(),
            "correct_answer": self.correct_answer,
            "keywords": self.keyword_list(),
            "created_at": self.created_at.strftime("%Y-%m-%d")
        }

    def __repr__(self):
        return f"<InterviewQ {self.id} [{self.category}]>"