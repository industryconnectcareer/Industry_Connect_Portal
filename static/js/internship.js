// =========================================
// internship.js - Internships Interactions
// =========================================

// -------- Filter Change Auto-Submit --------
document.addEventListener("change", (e) => {
    if (e.target.closest("[data-filter]")) {
        const form = document.querySelector("#internship-filter-form");
        if (form) form.submit();
    }
});

// -------- Search (Enter Key) --------
document.addEventListener("keydown", (e) => {
    if (e.target.matches("#internship-search") && e.key === "Enter") {
        e.preventDefault();
        document.querySelector("#internship-search-form").submit();
    }
});

// -------- Apply to Internship (AJAX) --------
document.addEventListener("click", async (e) => {
    if (e.target.matches("[data-apply-internship]")) {
        const internshipId = e.target.dataset.applyInternship;
        const btn = e.target;

        setButtonLoading(btn, true);

        try {
            const res = await fetch(`/internships/${internshipId}/apply`, {
                method: "POST",
                headers: { "X-Requested-With": "XMLHttpRequest" }
            });

            const result = await res.text();
            alert("Application submitted!");
        } catch (err) {
            alert("Something went wrong.");
            console.error(err);
        }

        setButtonLoading(btn, false);
    }
});

// -------- Bookmark Internship --------
document.addEventListener("click", async (e) => {
    if (e.target.matches("[data-bookmark]")) {
        const id = e.target.dataset.bookmark;

        await postJSON(
            "/student/bookmark",
            { internship_id: id },
            () => {
                e.target.classList.toggle("saved");
                alert("Saved to your list!");
            }
        );
    }
});

// -------- Load More Internships --------
document.addEventListener("click", (e) => {
    if (e.target.matches("#load-more")) {
        const hiddenItems = document.querySelectorAll(".internship-card.hidden");
        hiddenItems.forEach((item, index) => {
            if (index < 5) item.classList.remove("hidden");
        });
        if (document.querySelectorAll(".internship-card.hidden").length === 0) {
            e.target.remove();
        }
    }
});

// -------- Client-Side Quick Filter (Mode: Onsite/Hybrid/Remote) --------
document.addEventListener("click", (e) => {
    if (e.target.matches("[data-mode-filter]")) {
        const mode = e.target.dataset.modeFilter;
        const cards = document.querySelectorAll(".internship-card");

        cards.forEach(card => {
            if (mode === "all" || card.dataset.mode === mode) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    }
});