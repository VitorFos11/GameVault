(function () {
  const root = document.documentElement;
  const THEME_KEY = "gamevault-theme";

  function applyTheme(theme) {
    if (theme === "light") {
      root.setAttribute("data-theme", "light");
    } else if (theme === "dark") {
      root.removeAttribute("data-theme");
    } else if (window.matchMedia("(prefers-color-scheme: light)").matches) {
      root.setAttribute("data-theme", "light");
    } else {
      root.removeAttribute("data-theme");
    }
  }

  const saved = localStorage.getItem(THEME_KEY) || "dark";
  applyTheme(saved);

  document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const current = root.getAttribute("data-theme") === "light" ? "light" : "dark";
      const next = current === "light" ? "dark" : "light";
      localStorage.setItem(THEME_KEY, next);
      applyTheme(next);
    });
  });

  document.querySelectorAll("[data-theme-set]").forEach((el) => {
    el.addEventListener("change", () => {
      const v = el.value;
      localStorage.setItem(THEME_KEY, v);
      applyTheme(v);
    });
  });

  const sidebar = document.querySelector(".gv-sidebar");
  const toggle = document.querySelector("[data-sidebar-toggle]");
  if (sidebar && toggle) {
    toggle.addEventListener("click", () => sidebar.classList.toggle("collapsed"));
  }

  document.querySelectorAll("[data-modal-open]").forEach((trigger) => {
    trigger.addEventListener("click", () => {
      const id = trigger.getAttribute("data-modal-open");
      const modal = document.getElementById(id);
      if (modal) modal.classList.add("open");
    });
  });

  document.querySelectorAll("[data-modal-close]").forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.closest(".gv-modal-backdrop")?.classList.remove("open");
    });
  });

  const stack = document.querySelector(".gv-toast-stack");
  if (stack) {
    setTimeout(() => {
      stack.querySelectorAll(".gv-toast").forEach((t, i) => {
        setTimeout(() => t.remove(), 4000 + i * 500);
      });
    }, 100);
  }
})();
