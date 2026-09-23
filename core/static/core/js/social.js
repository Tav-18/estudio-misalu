// Redes sociales simuladas: muestra "Redirigiendo…" y luego la captura del perfil.
(() => {
    const dialog = document.querySelector("#social-dialog");
    if (!dialog) return;

    const urlEl = dialog.querySelector("#social-dialog-url");
    const nameEl = dialog.querySelector("#social-dialog-name");
    const titleEl = dialog.querySelector("#social-dialog-title");
    const img = dialog.querySelector("#social-dialog-image");
    const loading = dialog.querySelector(".social-loading");
    const view = dialog.querySelector(".social-view");
    const closeBtn = dialog.querySelector(".social-dialog-close");
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const REDIRECT_DELAY_MS = reduceMotion ? 0 : 900;
    let timer = null;

    const open = (button) => {
        const { socialName, socialUrl, socialImage, socialHandle } = button.dataset;
        clearTimeout(timer);
        urlEl.textContent = socialUrl;
        nameEl.textContent = socialName;
        titleEl.textContent = `Perfil de Misalú en ${socialName}`;
        img.alt = `Perfil de ${socialHandle} en ${socialName}`;
        img.src = socialImage;
        dialog.dataset.network = socialName.toLowerCase();
        loading.hidden = false;
        view.hidden = true;
        dialog.showModal();
        timer = setTimeout(() => {
            loading.hidden = true;
            view.hidden = false;
            view.scrollTop = 0;
        }, REDIRECT_DELAY_MS);
    };

    const close = () => {
        clearTimeout(timer);
        dialog.close();
    };

    document.querySelectorAll("[data-social-name]").forEach((button) => {
        button.addEventListener("click", () => open(button));
    });
    closeBtn.addEventListener("click", close);
    dialog.addEventListener("click", (event) => {
        if (event.target === dialog) close();  // clic fuera de la ventana
    });
})();

// Menú "Vacante": el enlace abre el juego en otra pestaña (target="_blank")
// y aquí la página baja a la sección de la vacante y la resalta.
(() => {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    document.querySelectorAll("[data-scroll-target]").forEach((link) => {
        link.addEventListener("click", () => {
            const target = document.querySelector(link.dataset.scrollTarget);
            if (!target) return;
            target.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
            target.querySelectorAll(".reveal").forEach((el) => el.classList.add("is-visible"));
            target.classList.remove("is-highlighted");
            void target.offsetWidth;  // reinicia la animación si se presiona varias veces
            target.classList.add("is-highlighted");
        });
    });
})();
