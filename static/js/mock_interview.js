// =========================================
// mock_interview.js - AI Mock Interview
// =========================================

let currentQuestion = 0;
let answers = {};
let timerInterval;

// -------- Start Interview --------
document.addEventListener("click", (e) => {
    if (e.target.matches("#start-interview")) {
        document.querySelector("#intro-screen").style.display = "none";
        document.querySelector("#question-section").style.display = "block";
        loadQuestion(0);
        startTimer(10 * 60); // 10 minutes
    }
});

// -------- Load Question --------
function loadQuestion(index) {
    const questions = document.querySelectorAll("[data-question]");
    const questionText = questions[index].dataset.question;

    document.querySelector("#question-text").textContent = questionText;
    document.querySelector("#answer-box").value = answers[index] || "";
}

// -------- Save Answer --------
document.querySelector("#answer-box").addEventListener("input", (e) => {
    answers[currentQuestion] = e.target.value;
});

// -------- Next Question --------
document.addEventListener("click", (e) => {
    if (e.target.matches("#next-question")) {
        currentQuestion++;
        const total = document.querySelectorAll("[data-question]").length;

        if (currentQuestion >= total) {
            finishInterview();
            return;
        }
        loadQuestion(currentQuestion);
    }
});

// -------- Timer --------
function startTimer(duration) {
    let timeLeft = duration;
    const timerEl = document.querySelector("#timer");

    timerInterval = setInterval(() => {
        const min = String(Math.floor(timeLeft / 60)).padStart(2, "0");
        const sec = String(timeLeft % 60).padStart(2, "0");

        timerEl.textContent = `${min}:${sec}`;

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            finishInterview();
        }

        timeLeft--;
    }, 1000);
}

// -------- Finish Interview & Send to AI --------
async function finishInterview() {
    clearInterval(timerInterval);

    document.querySelector("#question-section").style.display = "none";
    document.querySelector("#loading-section").style.display = "block";

    await postJSON(
        "/mock/submit",
        { answers },
        (result) => {
            document.querySelector("#loading-section").style.display = "none";
            document.querySelector("#result-section").style.display = "block";

            document.querySelector("#final-score").textContent = result.score;
            document.querySelector("#final-feedback").textContent = result.feedback;
        },
        () => alert("Error evaluating answers.")
    );
}