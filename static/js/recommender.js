// =======================================
// recommender.js - AI Recommendations UI
// =======================================

// -------- Load AI Recommendations --------
async function loadRecommendations() {
    const container = document.querySelector("#recommendations-container");
    const loader = document.querySelector("#recommendations-loader");

    if (!container || !loader) return;

    loader.style.display = "block";
    container.innerHTML = "";

    try {
        const res = await fetch("/student/recommendations", {
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        });

        if (!res.ok) {
            throw new Error("Failed to load recommendations");
        }

        const data = await res.json();

        if (!data.length) {
            container.innerHTML = `<p>No recommendations yet. Update your skills & tests to improve suggestions.</p>`;
        } else {
            data.forEach(item => {
                const card = document.createElement("div");
                card.className = "reco-card";
                card.innerHTML = `
                    <h4>${item.title}</h4>
                    <p><strong>Company:</strong> ${item.company || ""}</p>
                    <p><strong>Category:</strong> ${item.category}</p>
                    <p><strong>Match:</strong> ${item.match_score}%</p>

                    <button class="btn-apply-reco" data-apply-internship="${item.id}">
                        Apply
                    </button>

                    <button class="btn-skip-reco" data-not-interested="${item.id}">
                        Not Interested
                    </button>
                `;
                container.appendChild(card);
            });
        }
    } catch (err) {
        console.error(err);
        container.innerHTML = `<p>Error loading recommendations.</p>`;
    } finally {
        loader.style.display = "none";
    }
}

// -------- Not Interested --------
document.addEventListener("click", async (e) => {
    if (e.target.matches("[data-not-interested]")) {
        const internshipId = e.target.dataset.notInterested;
        const card = e.target.closest(".reco-card");

        await postJSON(
            "/student/recommendations/skip",
            { internship_id: internshipId },
            () => {
                if (card) card.remove();
            }
        );
    }
});

// -------- Refresh Recommendations --------
document.addEventListener("click", (e) => {
    if (e.target.matches("#refresh-recommendations")) {
        loadRecommendations();
    }
});

// Auto-load on page ready
document.addEventListener("DOMContentLoaded", () => {
    if (document.querySelector("#recommendations-container")) {
        loadRecommendations();
    }
});