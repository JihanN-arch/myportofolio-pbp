// *ERROR PER FIELD
// Menghapus semua pesan error API dan tanda merah di form
function clearFieldErrors(form) {
  form
    .querySelectorAll("[data-api-error]")
    .forEach((element) => element.remove());
  form
    .querySelectorAll('[aria-invalid="true"]')
    .forEach((input) => input.removeAttribute("aria-invalid"));
}

// Menampilkan error DRF tepat di bawah input yang salah
function showFieldErrors(form, fieldErrors = {}) {
  clearFieldErrors(form);
  let firstInvalid = null;
  Object.entries(fieldErrors).forEach(([name, messages]) => {
    const input = form.elements[name];
    if (!input || !Array.isArray(messages)) return;
    input.setAttribute("aria-invalid", "true");
    const message = document.createElement("p");
    message.className = "form-error";
    message.dataset.apiError = "";
    message.textContent = messages.join(" ");
    input.closest(".form-group").appendChild(message);
    firstInvalid ??= input;
  });
  firstInvalid?.focus();
}

// Pesan error satu field hilang saat user mulai memperbaikinya
function clearErrorOnInput(form) {
  form.addEventListener("input", function (event) {
    const input = event.target;
    if (input.getAttribute("aria-invalid") !== "true") return;
    input.removeAttribute("aria-invalid");
    input.closest(".form-group")?.querySelector("[data-api-error]")?.remove();
  });
}
