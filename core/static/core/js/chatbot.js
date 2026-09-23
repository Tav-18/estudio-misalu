(() => {
    const root = document.querySelector(".chatbot");
    if (!root) return;

    const endpoint = root.dataset.endpoint;
    const toggle = root.querySelector(".chatbot-toggle");
    const panel = root.querySelector(".chatbot-panel");
    const closeBtn = root.querySelector(".chatbot-close");
    const resetBtn = root.querySelector(".chatbot-reset");
    const messagesBox = root.querySelector(".chatbot-messages");
    const form = root.querySelector(".chatbot-form");
    const input = root.querySelector("#chatbot-input");
    const sendBtn = form.querySelector("button[type=submit]");
    const suggestions = root.querySelector(".chatbot-suggestions");

    const welcomeHTML = messagesBox.innerHTML;
    const history = [];
    const MAX_HISTORY = 8;
    let busy = false;

    const getCookie = (name) => {
        const match = document.cookie.match(new RegExp("(?:^|; )" + name + "=([^;]*)"));
        return match ? decodeURIComponent(match[1]) : "";
    };

    const setOpen = (open) => {
        panel.hidden = !open;
        root.classList.toggle("is-open", open);
        toggle.setAttribute("aria-expanded", String(open));
        toggle.setAttribute("aria-label", open ? "Cerrar asistente virtual" : "Abrir asistente virtual");
        if (open) input.focus();
    };

    const addMessage = (text, who) => {
        const el = document.createElement("div");
        el.className = `chatbot-msg chatbot-msg-${who}`;
        el.textContent = text;  // textContent evita inyectar HTML
        messagesBox.appendChild(el);
        messagesBox.scrollTop = messagesBox.scrollHeight;
        return el;
    };

    // Muestra el menú de opciones al final de la conversación.
    const showMenu = (show) => {
        suggestions.hidden = !show;
        if (show) messagesBox.scrollTop = messagesBox.scrollHeight;
    };

    const resetChat = () => {
        if (busy) return;
        history.length = 0;
        messagesBox.innerHTML = welcomeHTML;
        showMenu(true);
        input.value = "";
        input.focus();
    };

    const send = async (text) => {
        const message = text.trim();
        if (!message || busy) return;
        busy = true;
        sendBtn.disabled = true;
        showMenu(false);

        addMessage(message, "user");
        input.value = "";
        const typing = addMessage("Escribiendo…", "bot");
        typing.classList.add("chatbot-typing");

        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({ message, history: history.slice(-MAX_HISTORY) }),
            });
            const data = await response.json().catch(() => ({}));
            typing.remove();

            if (response.ok && data.reply) {
                addMessage(data.reply, "bot");
                history.push({ role: "user", text: message }, { role: "model", text: data.reply });
            } else {
                addMessage(data.error || "Ocurrió un error. Intenta de nuevo.", "error");
            }
        } catch (err) {
            typing.remove();
            addMessage("No hay conexión con el asistente. Revisa tu internet e inténtalo de nuevo.", "error");
        } finally {
            busy = false;
            sendBtn.disabled = false;
            showMenu(true);
            input.focus();
        }
    };

    toggle.addEventListener("click", () => setOpen(panel.hidden));
    resetBtn.addEventListener("click", resetChat);
    closeBtn.addEventListener("click", () => { setOpen(false); toggle.focus(); });
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && !panel.hidden) { setOpen(false); toggle.focus(); }
    });
    form.addEventListener("submit", (e) => { e.preventDefault(); send(input.value); });
    suggestions.querySelectorAll("button").forEach((btn) => {
        btn.addEventListener("click", () => send(btn.textContent));
    });
})();
