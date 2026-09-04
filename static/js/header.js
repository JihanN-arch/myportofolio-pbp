const header = document.querySelector("site-header");

window.addEventListener("scroll", () => {
  if (window.scroll > 30) {
    header.classList.add("scrolled");
  } else {
    header.classList.remove("scrolled");
  }
});
