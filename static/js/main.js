document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const loading = document.getElementById("loading");

    if (form && loading) {
        form.addEventListener("submit", () => {
            loading.style.display = "block";
        });
    }
});