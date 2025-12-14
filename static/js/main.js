// ===============================
// main.js - Global JS for Portal
// ===============================

// -------- Flash Messages Auto Hide --------
document.addEventListener("DOMContentLoaded", () => {
    const flashes = document.querySelectorAll(".flashes li");
    if (flashes.length > 0) {
        setTimeout(() => {
            flashes.forEach(f => {
                f.style.transition = "opacity 0.5s ease";
                f.style.opacity = "0";
                setTimeout(() => f.remove(), 600);
            });
        }, 4000); // 4 seconds visible
    }
});

// -------- Simple Fetch Helper (POST JSON) --------
async function postJSON(url, data, onSuccess, onError) {
    try {
        const res = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest"
            },
            body: JSON.stringify(data)
        });

        if (!res.ok) {
            throw new Error(`Request failed: ${res.status}`);
        }

        const result = await res.json();
        if (onSuccess) onSuccess(result);
    } catch (err) {
        console.error("postJSON error:", err);
        if (onError) onError(err);
    }
}

// -------- Button Loading State Helper --------
function setButtonLoading(btn, isLoading, textWhenDone = "Submit") {
    if (!btn) return;
    if (isLoading) {
        btn.dataset.originalText = btn.textContent;
        btn.textContent = "Please wait...";
        btn.disabled = true;
    } else {
        btn.textContent = btn.dataset.originalText || textWhenDone;
        btn.disabled = false;
    }
}

// -------- Mobile Nav Toggle (if you add hamburger later) --------
document.addEventListener("click", (e) => {
    const toggle = e.target.closest("[data-nav-toggle]");
    if (toggle) {
        const targetSelector = toggle.getAttribute("data-nav-toggle");
        const target = document.querySelector(targetSelector);
        if (target) {
            target.classList.toggle("nav-open");
        }
    }
});

// -------- Back to Top Button (optional) --------
const backToTopBtn = document.querySelector("[data-back-to-top]");

if (backToTopBtn) {
    window.addEventListener("scroll", () => {
        if (window.scrollY > 300) {
            backToTopBtn.style.display = "block";
        } else {
            backToTopBtn.style.display = "none";
        }
    });

    backToTopBtn.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
}

// -------- Expose helpers globally (if needed by other JS files) --------
window.postJSON = postJSON;
window.setButtonLoading = setButtonLoading;