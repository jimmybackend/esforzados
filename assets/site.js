(() => {
  "use strict";

  const carousel = document.querySelector(".carousel");
  const slides = carousel ? Array.from(carousel.querySelectorAll(".slide")) : [];
  const dots = carousel ? Array.from(carousel.querySelectorAll(".carousel-dot")) : [];
  const announcement = document.getElementById("carousel-announcement");
  const names = ["Esforzados Legal", "ArcadeCloud Drive", "Esforzados Hub", "Esforzados Edu", "Esforzados Chat"];
  let active = 0;
  let timer = null;
  let touchStartX = null;
  let pointerInside = false;
  let focusInside = false;

  const motionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");

  function goToSlide(index, announce = true) {
    if (!slides.length) return;
    active = (index + slides.length) % slides.length;

    slides.forEach((slide, i) => {
      const selected = i === active;
      slide.hidden = !selected;
      slide.classList.toggle("is-active", selected);
    });

    dots.forEach((dot, i) => {
      const selected = i === active;
      dot.classList.toggle("is-active", selected);
      if (selected) dot.setAttribute("aria-current", "true");
      else dot.removeAttribute("aria-current");
    });

    if (announce && announcement) {
      announcement.textContent = "Servicio " + (active + 1) + " de " + slides.length + ": " + names[active];
    }
  }

  function stopAutoplay() {
    if (timer !== null) {
      window.clearInterval(timer);
      timer = null;
    }
  }

  function startAutoplay() {
    stopAutoplay();
    if (!carousel || slides.length <= 1 || motionPreference.matches ||
        document.hidden || pointerInside || focusInside) return;

    timer = window.setInterval(() => {
      goToSlide(active + 1, false);
    }, 8500);
  }

  if (carousel && slides.length === dots.length && slides.length > 0) {
    goToSlide(0, false);

    dots.forEach((dot, i) => {
      dot.addEventListener("click", () => {
        goToSlide(i);
        startAutoplay();
      });
    });

    carousel.querySelector(".carousel-prev")?.addEventListener("click", () => {
      goToSlide(active - 1);
      startAutoplay();
    });

    carousel.querySelector(".carousel-next")?.addEventListener("click", () => {
      goToSlide(active + 1);
      startAutoplay();
    });

    carousel.addEventListener("keydown", event => {
      if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
      if (event.target instanceof HTMLElement && event.target.closest("a")) return;
      event.preventDefault();
      goToSlide(active + (event.key === "ArrowRight" ? 1 : -1));
    });

    carousel.addEventListener("touchstart", event => {
      if (event.touches.length === 1) touchStartX = event.touches[0].clientX;
    }, {passive: true});

    carousel.addEventListener("touchend", event => {
      if (touchStartX === null || event.changedTouches.length !== 1) return;
      const delta = event.changedTouches[0].clientX - touchStartX;
      touchStartX = null;
      if (Math.abs(delta) >= 55) {
        goToSlide(active + (delta < 0 ? 1 : -1));
        startAutoplay();
      }
    }, {passive: true});

    carousel.addEventListener("touchcancel", () => { touchStartX = null; });
    carousel.addEventListener("pointerenter", () => { pointerInside = true; stopAutoplay(); });
    carousel.addEventListener("pointerleave", () => { pointerInside = false; startAutoplay(); });
    carousel.addEventListener("focusin", () => { focusInside = true; stopAutoplay(); });
    carousel.addEventListener("focusout", event => {
      const next = event.relatedTarget;
      focusInside = next instanceof Node && carousel.contains(next);
      startAutoplay();
    });

    document.addEventListener("visibilitychange", startAutoplay);
    if (typeof motionPreference.addEventListener === "function") {
      motionPreference.addEventListener("change", startAutoplay);
    }
    startAutoplay();
  }

  const menuButton = document.querySelector(".menu-toggle");
  const menu = document.getElementById("menu-principal");

  function setMenuOpen(open) {
    if (!menu || !menuButton) return;
    menu.classList.toggle("is-open", open);
    menuButton.setAttribute("aria-expanded", String(open));
    menuButton.setAttribute("aria-label", open ? "Cerrar menú de navegación" : "Abrir menú de navegación");
  }

  if (menuButton && menu) {
    menuButton.addEventListener("click", () => {
      setMenuOpen(menuButton.getAttribute("aria-expanded") !== "true");
    });

    menu.querySelectorAll("a").forEach(link => link.addEventListener("click", () => setMenuOpen(false)));

    document.addEventListener("keydown", event => {
      if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
        setMenuOpen(false);
        menuButton.focus();
      }
    });

    document.addEventListener("click", event => {
      if (event.target instanceof Node &&
          !menu.contains(event.target) && !menuButton.contains(event.target)) setMenuOpen(false);
    });

    window.matchMedia("(min-width: 761px)").addEventListener?.("change", event => {
      if (event.matches) setMenuOpen(false);
    });
  }

  const year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();
