// ======================================
// employer.js - Employer Dashboard Logic
// ======================================

// ------- Internship Post Submit -------
document.addEventListener("submit", (e) => {
    if (e.target.matches("#post-internship-form")) {
        const btn = document.querySelector("#post-internship-btn");
        setButtonLoading(btn, true, "Posted");
    }
});

// ------- Verify Docs Upload Preview -------
document.addEventListener("change", (e) => {
    if (e.target.matches(".doc-upload")) {
        const file = e.target.files[0];
        if (file) {
            const label = e.target.closest(".doc-item").querySelector(".doc-name");
            label.textContent = file.name;
        }
    }
});

// ------- Application Shortlist / Reject / Select -------
async function updateApplicationStatus(appID, status) {
    try {
        await postJSON(`/employer/applications/${appID}`, { status });
        alert(`Student ${status} successfully!`);
        location.reload();
    } catch (err) {
        alert("Failed to update status.");
        console.error(err);
    }
}

document.addEventListener("click", (e) => {
    if (e.target.matches("[data-shortlist]")) {
        updateApplicationStatus(e.target.dataset.shortlist, "shortlisted");
    }
    if (e.target.matches("[data-reject]")) {
        updateApplicationStatus(e.target.dataset.reject, "rejected");
    }
    if (e.target.matches("[data-select]")) {
        updateApplicationStatus(e.target.dataset.select, "selected");
    }
});

// ------- Dashboard Stats Count Animation -------
document.addEventListener("DOMContentLoaded", () => {
    const counters = document.querySelectorAll("[data-counter]");

    counters.forEach(counter => {
        let current = 0;
        const target = parseInt(counter.dataset.counter);
        
        const inc = Math.ceil(target / 40);

        const update = setInterval(() => {
            current += inc;
            counter.textContent = current;
            if (current >= target) {
                counter.textContent = target;
                clearInterval(update);
            }
        }, 30);
    });
});