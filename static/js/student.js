// ===============================
// student.js - Student Dashboard
// ===============================

// ------- Apply to Internship (AJAX) -------
document.addEventListener("click", async (e) => {
    if (e.target.matches("[data-apply]")) {
        const internshipId = e.target.dataset.apply;
        const btn = e.target;

        setButtonLoading(btn, true);

        try {
            const res = await fetch(`/internships/${internshipId}/apply`, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            const data = await res.text();
            alert("Application submitted!");
        } catch (err) {
            alert("Error applying!");
            console.error(err);
        }

        setButtonLoading(btn, false);
    }
});

// ------- Saved Search -------
document.addEventListener("click", async (e) => {
    if (e.target.matches("[data-save-search]")) {
        const query = e.target.dataset.query;
        
        await postJSON(
            "/student/save-search",
            { query },
            () => alert("Search saved successfully!")
        );
    }
});

// ------- Resume Upload Preview -------
document.addEventListener("change", (e) => {
    if (e.target.matches("#resume-upload")) {
        const file = e.target.files[0];
        if (file) {
            document.querySelector("#resume-name").textContent = file.name;
        }
    }
});

// ------- Skill Badge Tooltip -------
document.addEventListener("mouseover", (e) => {
    if (e.target.matches(".badge-item")) {
        const info = e.target.dataset.info;
        const tooltip = document.querySelector("#badge-tooltip");
        tooltip.textContent = info;
        tooltip.style.display = "block";
    }
});

document.addEventListener("mouseout", (e) => {
    if (e.target.matches(".badge-item")) {
        document.querySelector("#badge-tooltip").style.display = "none";
    }
});

// ------- Readiness Score Circle Animation -------
function animateScore() {
    const circle = document.querySelector("[data-score-circle]");
    if (!circle) return;

    const score = parseInt(circle.dataset.score);
    let current = 0;

    const interval = setInterval(() => {
        current++;
        circle.style.setProperty("--score", current);
        if (current >= score) clearInterval(interval);
    }, 20);
}

document.addEventListener("DOMContentLoaded", animateScore);