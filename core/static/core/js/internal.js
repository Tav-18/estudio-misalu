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

    // ---------- Recursos Humanos: explorador de expedientes ----------
    // Sin JavaScript cada candidato es un enlace (?exp=slug); con JavaScript cambia sin recargar.
    const explorer = document.querySelector("[data-exp-explorer]");
    if (explorer) {
        const links = Array.from(explorer.querySelectorAll("[data-exp-target]"));
        const panels = explorer.querySelectorAll("[data-exp-panel]");
        const select = (slug, focusPanel = false) => {
            links.forEach((link) => {
                if (link.dataset.expTarget === slug) link.setAttribute("aria-current", "true");
                else link.removeAttribute("aria-current");
            });
            panels.forEach((panel) => { panel.hidden = panel.dataset.expPanel !== slug; });
            const url = new URL(window.location);
            url.searchParams.set("tab", "rh");
            url.searchParams.set("exp", slug);
            history.replaceState(null, "", url);
            if (focusPanel) {
                const panel = explorer.querySelector(`[data-exp-panel="${slug}"]`);
                // En celular la lista queda arriba: lleva la vista al expediente elegido.
                if (window.matchMedia("(max-width: 900px)").matches) {
                    panel?.scrollIntoView({ behavior: "smooth", block: "start" });
                }
            }
        };
        links.forEach((link, index) => {
            link.addEventListener("click", (event) => {
                event.preventDefault();
                select(link.dataset.expTarget, true);
            });
            link.addEventListener("keydown", (event) => {
                if (!["ArrowDown", "ArrowUp", "ArrowRight", "ArrowLeft"].includes(event.key)) return;
                event.preventDefault();
                const visible = links.filter((l) => !l.closest("li").hidden);
                const pos = visible.indexOf(link);
                const step = event.key === "ArrowDown" || event.key === "ArrowRight" ? 1 : -1;
                const next = visible[(pos + step + visible.length) % visible.length];
                next?.focus();
                if (next) select(next.dataset.expTarget);
            });
        });

        const searchInput = explorer.querySelector("[data-exp-search]");
        const emptyMsg = explorer.querySelector("[data-exp-empty]");
        searchInput?.addEventListener("input", () => {
            const needle = normalize(searchInput.value.trim());
            let shown = 0;
            explorer.querySelectorAll("[data-exp-item]").forEach((item) => {
                const match = !needle || normalize(item.dataset.search).includes(needle);
                item.hidden = !match;
                if (match) shown += 1;
            });
            if (emptyMsg) emptyMsg.hidden = shown > 0;
        });
    }

    // Sub-navegación de RH: desplazamiento suave respetando "reducir movimiento".
    document.querySelectorAll('.rh-subnav a[href^="#"], a[href="#expedientes"]').forEach((link) => {
        link.addEventListener("click", (event) => {
            const target = document.querySelector(link.getAttribute("href"));
            if (!target) return;
            event.preventDefault();
            const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
            target.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
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
