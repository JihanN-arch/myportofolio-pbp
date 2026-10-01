document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) lucide.createIcons();
});

document.addEventListener("click", (event) => {
  const btn = event.target.closest(".experience-toggle");
  if (!btn) return;

  const card = btn.closest(".experience-card");
  const expanded = btn.getAttribute("aria-expanded") === "true";

  btn.setAttribute("aria-expanded", String(!expanded));
  card.classList.toggle("is-open", !expanded);
});
