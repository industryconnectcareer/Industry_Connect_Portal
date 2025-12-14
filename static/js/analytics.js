// =======================================
// analytics.js - Admin Analytics Charts
// =======================================

// Load analytics data from backend and draw charts
async function loadAnalytics() {
    const rolesCtx = document.getElementById("chart-demanded-roles");
    const regsCtx = document.getElementById("chart-student-registrations");

    try {
        const res = await fetch("/analytics/data", {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        });
        if (!res.ok) throw new Error("Failed to load analytics");

        const data = await res.json();
        // Expecting:
        // data = {
        //   demanded_roles: { labels: [...], values: [...] },
        //   registrations: { labels: [...], values: [...] }
        // }

        if (rolesCtx && data.demanded_roles) {
            new Chart(rolesCtx, {
                type: "bar",
                data: {
                    labels: data.demanded_roles.labels,
                    datasets: [{
                        label: "Most Demanded Roles",
                        data: data.demanded_roles.values
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }

        if (regsCtx && data.registrations) {
            new Chart(regsCtx, {
                type: "line",
                data: {
                    labels: data.registrations.labels,
                    datasets: [{
                        label: "Student Registrations",
                        data: data.registrations.values,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }

    } catch (err) {
        console.error("Analytics error:", err);
    }
}

// Animate numeric KPI cards (e.g., Total Students, Total Internships)
function animateKPI() {
    const kpis = document.querySelectorAll("[data-kpi]");

    kpis.forEach(el => {
        let current = 0;
        const target = parseInt(el.dataset.kpi) || 0;

        const inc = Math.max(1, Math.ceil(target / 40));

        const interval = setInterval(() => {
            current += inc;
            el.textContent = current;
            if (current >= target) {
                el.textContent = target;
                clearInterval(interval);
            }
        }, 40);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("chart-demanded-roles") ||
        document.getElementById("chart-student-registrations")) {
        loadAnalytics();
    }
    animateKPI();
});