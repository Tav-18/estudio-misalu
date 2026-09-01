(() => {
    const menuButton = document.querySelector(".menu-toggle");
    const nav = document.querySelector(".main-nav");

    if (menuButton && nav) {
        const closeMenu = () => {
            nav.classList.remove("open");
            document.body.classList.remove("menu-open");
            menuButton.setAttribute("aria-expanded", "false");
            menuButton.setAttribute("aria-label", "Abrir menú");
        };

        menuButton.addEventListener("click", () => {
            const isOpen = nav.classList.toggle("open");
            document.body.classList.toggle("menu-open", isOpen);
            menuButton.setAttribute("aria-expanded", String(isOpen));
            menuButton.setAttribute("aria-label", isOpen ? "Cerrar menú" : "Abrir menú");
        });

        nav.querySelectorAll("a").forEach(link => {
            link.addEventListener("click", closeMenu);
        });

        window.addEventListener("resize", () => {
            if (window.innerWidth > 980) closeMenu();
        });
    }

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const revealItems = document.querySelectorAll(".reveal");

    if (!reduceMotion && "IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.14 });

        revealItems.forEach(el => observer.observe(el));
    } else {
        revealItems.forEach(el => el.classList.add("is-visible"));
    }

    const dialog = document.querySelector("#gallery-dialog");
    const dialogTitle = document.querySelector("#dialog-title");
    const closeButton = dialog?.querySelector(".dialog-close");

    document.querySelectorAll(".gallery-tile").forEach(tile => {
        tile.addEventListener("click", () => {
            if (!dialog) return;
            dialogTitle.textContent = tile.dataset.label || "Galería Misalú";
            if (typeof dialog.showModal === "function") dialog.showModal();
        });
    });

    closeButton?.addEventListener("click", () => dialog.close());

    dialog?.addEventListener("click", (event) => {
        const rect = dialog.getBoundingClientRect();
        const clickedOutside =
            event.clientX < rect.left ||
            event.clientX > rect.right ||
            event.clientY < rect.top ||
            event.clientY > rect.bottom;
        if (clickedOutside) dialog.close();
    });
})();
