from flask import Blueprint, render_template, request, session
from flask_login import login_required, current_user
from ai.mock_interview_ai import generate_question, evaluate_answer, get_hint, get_followup_question

mock_bp = Blueprint("mock", __name__, url_prefix="/mock")

# ---------------------------------------------------------
# INITIALIZE ATTEMPT HISTORY IN SESSION
# ---------------------------------------------------------
def init_history():
    if "mock_history" not in session:
        session["mock_history"] = []


# ---------------------------------------------------------
# MOCK INTERVIEW MAIN PAGE
# ---------------------------------------------------------
@mock_bp.route("/", methods=["GET", "POST"])
@login_required
def mock_interview():

    init_history()

    # -----------------------------
    # FORM SUBMISSION — USER ANSWERS
    # -----------------------------
    if request.method == "POST":
        question = request.form.get("question")
        answer = request.form.get("answer")
        category = request.form.get("category")
        difficulty = request.form.get("difficulty")

        # Evaluate answer (AI)
        feedback, score = evaluate_answer(question, answer)

        # Optional: follow-up question
        followup = get_followup_question(question)

        # Add history entry
        session["mock_history"].insert(0, {
            "question": question,
            "answer": answer,
            "feedback": feedback,
            "score": score
        })

        # Limit to last 5 attempts
        session["mock_history"] = session["mock_history"][:5]

        return render_template(
            "student/mock_interview.html",
            question=generate_question(category, difficulty),
            category=category,
            difficulty=difficulty,
            feedback=feedback,
            score=score,
            followup=followup,
            hint=None,
            history=session["mock_history"]
        )

    # -----------------------------
    # INITIAL PAGE LOAD
    # -----------------------------
    category = request.args.get("category", "General Commerce")
    difficulty = request.args.get("difficulty", "Medium")

    question = generate_question(category, difficulty)
    hint = get_hint(question)

    return render_template(
        "student/mock_interview.html",
        question=question,
        category=category,
        difficulty=difficulty,
        feedback=None,
        score=None,
        followup=None,
        hint=hint,
        history=session["mock_history"]
    )