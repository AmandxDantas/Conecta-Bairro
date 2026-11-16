(() => {
  const toggle = document.querySelector("[data-menu-toggle]");
  const menu = document.querySelector("[data-menu]");

  if (toggle && menu) {
    toggle.addEventListener("click", () => {
      const isOpen = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!isOpen));
      const label = toggle.querySelector(".sr-only");
      if (label) label.textContent = isOpen ? "Abrir menu" : "Fechar menu";
      menu.classList.toggle("is-open", !isOpen);
    });

    menu.addEventListener("click", (event) => {
      if (event.target.closest("a")) {
        toggle.setAttribute("aria-expanded", "false");
        menu.classList.remove("is-open");
      }
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && menu.classList.contains("is-open")) {
        toggle.setAttribute("aria-expanded", "false");
        menu.classList.remove("is-open");
        toggle.focus();
      }
    });
  }

  document.querySelectorAll("[data-dismiss]").forEach((button) => {
    button.addEventListener("click", () => button.closest(".message")?.remove());
  });
})();
