// =========================================
// ojt.js - OJT Panels & Enroll Handling
// =========================================

// -------- Expand / Collapse Module Details --------
document.addEventListener("click", (e) => {
    if (e.target.matches(".ojt-module-header")) {
        const content = e.target.nextElementSibling;
        content.classList.toggle("open");
    }
});

// -------- Enroll in OJT (AJAX) --------
document.addEventListener("click", async (e) => {
    if (e.target.matches("[data-ojt-enroll]")) {
        const id = e.target.dataset.ojtEnroll;
        const btn = e.target;

        setButtonLoading(btn, true);

        await postJSON(
            `/ojt/${id}/enroll`,
            {},
            () => alert("You are now enrolled!"),
            () => alert("Enrollment failed.")
        );

        setButtonLoading(btn, false);
    }
});

// -------- Module Progress Animation --------
function animateOJTProgress() {
    const bars = document.querySelectorAll("[data-ojt-progress]");
    bars.forEach(bar => {
        const val = parseInt(bar.dataset.ojtProgress);
        bar.style.width = "0%";
        setTimeout(() => {
            bar.style.transition = "width 1.2s ease";
            bar.style.width = val + "%";
        }, 100);
    });
}

document.addEventListener("DOMContentLoaded", animateOJTProgress);

// -------- Certificate Ready Popup --------
document.addEventListener("click", (e) => {
    if (e.target.matches("[data-certificate-ready]")) {
        alert("🎉 Your OJT Certificate is ready for download!");
    }
});