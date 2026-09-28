// Área interna: pestañas, filtros en vivo de trabajadores y filtro de procesos de RH.
(() => {
    const normalize = (text) =>
        String(text || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");

    // ---------- Pestañas ----------
    const tabs = document.querySelectorAll(".internal-tab");
    const showTab = (name, updateUrl = true) => {
        tabs.forEach((tab) => {
            const active = tab.dataset.tab === name;
            tab.setAttribute("aria-selected", String(active));
            tab.tabIndex = active ? 0 : -1;
            const panel = document.getElementById(tab.getAttribute("aria-controls"));
            if (panel) panel.hidden = !active;
        });
        if (updateUrl) {
            const url = new URL(window.location);
            url.searchParams.set("tab", name);
            history.replaceState(null, "", url);
        }
    };
    tabs.forEach((tab, index) => {
        tab.addEventListener("click", (event) => {
            event.preventDefault();
            showTab(tab.dataset.tab);
        });
        tab.addEventListener("keydown", (event) => {
            if (event.key !== "ArrowRight" && event.key !== "ArrowLeft") return;
            const next = tabs[(index + (event.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length];
            next.focus();
            showTab(next.dataset.tab);
        });
    });
    document.querySelectorAll("[data-go-tab]").forEach((link) => {
        link.addEventListener("click", (event) => {
            event.preventDefault();
            showTab(link.dataset.goTab);
            document.querySelector(".internal-tabs")?.scrollIntoView({ behavior: "smooth", block: "start" });
        });
    });

    // ---------- Trabajadores: filtros que se actualizan solos ----------
    const form = document.querySelector("[data-worker-filters]");
    if (form) {
        const search = form.querySelector('input[name="q"]');
        const selects = form.querySelectorAll("select[data-filter]");
        const rows = document.querySelectorAll("tr[data-worker]");
        const count = document.querySelector("[data-worker-count]");
        const empty = document.querySelector("[data-worker-empty]");

        form.querySelector("[data-no-js-submit]")?.setAttribute("hidden", "");

        const apply = () => {
            const needle = normalize(search.value.trim());
            let visible = 0;
            rows.forEach((row) => {
                let match = !needle || row.dataset.search.includes(needle);
                selects.forEach((select) => {
                    if (select.value && row.dataset[select.dataset.filter] !== select.value) match = false;
                });
                row.hidden = !match;
                if (match) visible += 1;
            });
            count.textContent = visible;
            empty.hidden = visible > 0;

            const url = new URL(window.location);
            url.searchParams.set("tab", "trabajadores");
            ["q", ...Array.from(selects, (s) => s.name)].forEach((key) => url.searchParams.delete(key));
            if (search.value.trim()) url.searchParams.set("q", search.value.trim());
            selects.forEach((s) => { if (s.value) url.searchParams.set(s.name, s.value); });
            history.replaceState(null, "", url);
        };

        search.addEventListener("input", apply);
        selects.forEach((select) => select.addEventListener("change", apply));
        form.addEventListener("submit", (event) => { event.preventDefault(); apply(); });
        form.querySelector("[data-clear-filters]")?.addEventListener("click", (event) => {
            event.preventDefault();
            search.value = "";
            selects.forEach((select) => { select.value = ""; });
            apply();
            search.focus();
        });
    }

    // ---------- Recursos Humanos: filtro por proceso ----------
    const chips = document.querySelectorAll("[data-hr-filter]");
    const cards = document.querySelectorAll("[data-hr-card]");
    const grid = document.querySelector(".hr-grid");
    chips.forEach((chip) => {
        chip.addEventListener("click", () => {
            const slug = chip.dataset.hrFilter;
            chips.forEach((c) => c.setAttribute("aria-pressed", String(c === chip)));
            cards.forEach((card) => { card.hidden = Boolean(slug) && card.dataset.hrCard !== slug; });
            grid?.classList.toggle("is-single", Boolean(slug));
        });
    });

    // ---------- Login: mostrar u ocultar la contraseña ----------
    const passwordInput = document.querySelector('.login-form input[name="password"]');
    document.querySelector("[data-password-toggle]")?.addEventListener("click", (event) => {
        const show = passwordInput.type === "password";
        passwordInput.type = show ? "text" : "password";
        event.currentTarget.textContent = show ? "Ocultar" : "Ver";
        event.currentTarget.setAttribute("aria-label", show ? "Ocultar contraseña" : "Mostrar contraseña");
    });

    // ---------- Confirmar antes de eliminar ----------
    document.querySelectorAll("form[data-confirm]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            if (!window.confirm(form.dataset.confirm)) event.preventDefault();
        });
    });
})();
