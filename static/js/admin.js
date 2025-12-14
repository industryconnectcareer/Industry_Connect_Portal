// ==================================
// admin.js - Admin Panel Operations
// ==================================

// ------- Approve Employer -------
document.addEventListener("click", async (e) => {
    if (e.target.matches("[data-approve-employer]")) {
        const id = e.target.dataset.approveEmployer;

        await postJSON(`/admin/employer/${id}/approve`, {}, () => {
            alert("Employer approved!");
            location.reload();
        });
    }
});

// ------- Reject Employer -------
document.addEventListener("click", async (e) => {
    if (e.target.matches("[data-reject-employer]")) {
        const id = e.target.dataset.rejectEmployer;

        await postJSON(`/admin/employer/${id}/reject`, {}, () => {
            alert("Employer rejected.");
            location.reload();
        });
    }
});

// ------- Verify Internship Posting -------
document.addEventListener("click", async (e) => {
    if (e.target.matches("[data-verify-posting]")) {
        const id = e.target.dataset.verifyPosting;

        await postJSON(`/admin/internship/${id}/verify`, {}, () => {
            alert("Internship verified!");
            location.reload();
        });
    }
});

// ------- Admin Analytics Loading -------
document.addEventListener("DOMContentLoaded", () => {
    const charts = document.querySelectorAll(".analytics-chart");

    charts.forEach(chart => {
        chart.classList.add("chart-loaded");
    });
});