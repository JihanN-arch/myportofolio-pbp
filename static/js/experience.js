document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) lucide.createIcons();

  document.querySelectorAll(".experience-toggle").forEach((btn) => {
    btn.addEventListener("click", () => {
      const card = btn.closest(".experience-card");
      const expanded = btn.getAttribute("aria-expanded") === "true";

      btn.setAttribute("aria-expanded", String(!expanded));
      card.classList.toggle("is-open", !expanded);
    });
  });
});
