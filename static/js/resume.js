// =====================================
// resume.js - Resume Scan & Scoring UI
// =====================================

const resumeInput = document.querySelector("#resume-upload-input");
const resumeScanBtn = document.querySelector("#resume-scan-btn");
const resumeScoreEl = document.querySelector("#resume-score");
const resumeFeedbackEl = document.querySelector("#resume-feedback");
const resumeProgressBar = document.querySelector("#resume-progress-bar");

// ------- Show selected file name -------
if (resumeInput) {
    resumeInput.addEventListener("change", () => {
        const file = resumeInput.files[0];
        const label = document.querySelector("#resume-file-name");
        if (file && label) label.textContent = file.name;
    });
}

// ------- Trigger Resume Scan (using FormData) -------
if (resumeScanBtn) {
    resumeScanBtn.addEventListener("click", async () => {
        if (!resumeInput || !resumeInput.files[0]) {
            alert("Please upload a resume first.");
            return;
        }

        const btn = resumeScanBtn;
        setButtonLoading(btn, true, "Scanning...");

        const formData = new FormData();
        formData.append("resume", resumeInput.files[0]);

        try {
            const res = await fetch("/student/resume/scan", {
                method: "POST",
                body: formData
            });

            if (!res.ok) throw new Error("Failed to scan resume");

            const data = await res.json(); // { score: 0-100, feedback: "..." }

            if (resumeScoreEl) resumeScoreEl.textContent = data.score;
            if (resumeFeedbackEl) resumeFeedbackEl.textContent = data.feedback;

            if (resumeProgressBar) {
                resumeProgressBar.style.width = "0%";
                setTimeout(() => {
                    resumeProgressBar.style.transition = "width 1s ease";
                    resumeProgressBar.style.width = data.score + "%";
                }, 100);
            }
        } catch (err) {
            console.error(err);
            alert("Error scanning resume.");
        }

        setButtonLoading(btn, false, "Scan Again");
    });
}