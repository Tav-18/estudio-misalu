import json
import unicodedata
from collections import Counter
from functools import wraps

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .chatbot import ChatbotError, ask_gemini, is_rate_limited, local_answer
from .data import (
    CLASSES, DEMO_ACCOUNTS, DEMO_CONTACT, GALLERY, HR_CAMPAIGN, HR_PROCESSES, INTERNAL_ROLES,
    PESTEL, SCHEDULE, SOCIAL_NETWORKS, VACANCY_CAMPAIGN, VACANCY_URL, VALUES, WORKER_FILTERS,
)
from .forms import ContactMessageForm, InternalLoginForm, WorkerForm
from .models import Worker

MAX_MESSAGE_LENGTH = 500
MAX_HISTORY_TURNS = 8


def _common_context():
    return {
        "classes": CLASSES,
        "schedule": SCHEDULE,
        "values": VALUES,
        "gallery": GALLERY,
        "demo_contact": DEMO_CONTACT,
        "social_networks": SOCIAL_NETWORKS,
        "vacancy_url": VACANCY_URL,
    }

@ensure_csrf_cookie
def home(request):
    form = ContactMessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "¡Gracias! una persona de nuestro equipo se contactara con usted.")
        return redirect("core:home")
    context = _common_context()
    context["form"] = form
    return render(request, "core/home.html", context)

@ensure_csrf_cookie
def project_info(request):
    context = _common_context()
    context["pestel"] = PESTEL
    return render(request, "core/project_info.html", context)


def _normalize(text):
    """Minúsculas y sin acentos, para que 'jose' encuentre a 'José'."""
    text = unicodedata.normalize("NFD", str(text).lower())
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn")


def _personal_stats(workers):
    active = [w for w in workers if w["estatus"] == "Activo"]
    by_area = Counter(w["area"] for w in active)
    max_area = max(by_area.values()) if by_area else 1
    return {
        "total": len(workers),
        "active": len(active),
        "inactive": len(workers) - len(active),
        "full_time": sum(1 for w in active if w["tipo"] == "Tiempo completo"),
        "part_time": sum(1 for w in active if w["tipo"] == "Medio tiempo"),
        "teachers": sum(1 for w in active if w["puesto"] == "Docente"),
        "by_area": [
            {"area": area, "count": count, "pct": round(count * 100 / max_area)}
            for area, count in by_area.most_common()
        ],
    }


# ---------- Acceso al Área interna (login de demostración) ----------
SESSION_KEY = "internal_user"


def _internal_user(request):
    """Devuelve la cuenta con sesión iniciada (con sus permisos) o None."""
    data = request.session.get(SESSION_KEY)
    if not data or data.get("role") not in INTERNAL_ROLES:
        return None
    return {**data, **INTERNAL_ROLES[data["role"]], "role": data["role"]}


def internal_required(permission=None):
    """Exige sesión en el Área interna y, opcionalmente, un permiso (can_view_rh / can_edit)."""
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            user = _internal_user(request)
            if user is None:
                return redirect(f"{reverse('core:internal_login')}?next={request.get_full_path()}")
            if permission and not user[permission]:
                messages.error(request, "Tu cuenta no tiene permiso para hacer eso.")
                return redirect("core:internal_area")
            request.internal_user = user
            return view(request, *args, **kwargs)
        return wrapper
    return decorator


@ensure_csrf_cookie
def internal_login(request):
    if _internal_user(request):
        return redirect("core:internal_area")
    form = InternalLoginForm(request.POST or None)
    error = ""
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"].strip().lower()
        account = next((a for a in DEMO_ACCOUNTS if a["email"] == email), None)
        if account and account["password"] == form.cleaned_data["password"]:
            request.session.cycle_key()
            request.session[SESSION_KEY] = {"email": account["email"], "name": account["name"], "role": account["role"]}
            next_url = request.GET.get("next", "")
            if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                next_url = reverse("core:internal_area")
            return redirect(next_url)
        error = "Correo o contraseña incorrectos."
    elif request.method == "POST":
        error = "Escribe un correo válido y tu contraseña."
    profiles = [{"key": key, **role} for key, role in INTERNAL_ROLES.items()]
    return render(request, "core/internal_login.html", {"form": form, "error": error, "profiles": profiles})


@require_POST
def internal_logout(request):
    request.session.pop(SESSION_KEY, None)
    return redirect("core:internal_login")


@ensure_csrf_cookie
@internal_required()
def internal_area(request):
    """Portal interno: directorio filtrable de trabajadores y procesos de RH.

    Los filtros funcionan con parámetros GET (?puesto=Docente&q=ana) para que la página sirva
    aun sin JavaScript; con JavaScript, internal.js filtra al instante sin recargar.
    """
    user = request.internal_user
    selected = {f["key"]: request.GET.get(f["key"], "") for f in WORKER_FILTERS}
    query = request.GET.get("q", "").strip()[:60]
    needle = _normalize(query)

    workers = list(Worker.objects.values("id", "nombre", "cargo", "puesto", "area", "disciplina", "tipo", "estatus", "ingreso"))
    rows = []
    for worker in workers:
        matches = all(not value or worker[key] == value for key, value in selected.items())
        search = _normalize(f"{worker['nombre']} {worker['cargo']}")
        if needle:
            matches = matches and needle in search
        rows.append({**worker, "search": search, "visible": matches})

    filters = [{**f, "selected": selected[f["key"]]} for f in WORKER_FILTERS]
    tab = "rh" if request.GET.get("tab") == "rh" else "trabajadores"
    context = _common_context()
    context.update({
        "internal_user": user,
        "filters": filters,
        "query": query,
        "workers": rows,
        "visible_count": sum(1 for r in rows if r["visible"]),
        "hr_processes": HR_PROCESSES if user["can_view_rh"] else [],
        "hr_campaign": HR_CAMPAIGN if user["can_view_rh"] else None,
        "vacancy_campaign": VACANCY_CAMPAIGN,
        "stats": _personal_stats(workers),
        "active_tab": tab,
    })
    return render(request, "core/internal_area.html", context)


@ensure_csrf_cookie
@internal_required("can_edit")
def worker_form(request, pk=None):
    worker = get_object_or_404(Worker, pk=pk) if pk else None
    form = WorkerForm(request.POST or None, instance=worker)
    if request.method == "POST" and form.is_valid():
        saved = form.save()
        verb = "actualizado" if worker else "agregado"
        messages.success(request, f"Trabajador {verb}: {saved.nombre}.")
        return redirect("core:internal_area")
    return render(request, "core/internal_worker_form.html",
                  {"form": form, "worker": worker, "internal_user": request.internal_user})


@require_POST
@internal_required("can_edit")
def worker_delete(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    messages.success(request, f"Trabajador eliminado: {worker.nombre}.")
    worker.delete()
    return redirect("core:internal_area")


def _clean_history(raw_history):
    """Valida el historial enviado por el navegador y conserva los últimos turnos."""
    if not isinstance(raw_history, list):
        return []
    history = []
    for turn in raw_history[-MAX_HISTORY_TURNS:]:
        if not isinstance(turn, dict):
            continue
        role = turn.get("role")
        text = str(turn.get("text", "")).strip()[:MAX_MESSAGE_LENGTH * 2]
        if role in ("user", "model") and text:
            history.append({"role": role, "text": text})
    return history


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "desconocida")


@require_POST
def chat_api(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({"error": "Solicitud inválida."}, status=400)

    message = str(payload.get("message", "")).strip()
    if not message:
        return JsonResponse({"error": "Escribe una pregunta."}, status=400)
    if len(message) > MAX_MESSAGE_LENGTH:
        return JsonResponse(
            {"error": f"La pregunta es muy larga (máximo {MAX_MESSAGE_LENGTH} caracteres)."},
            status=400,
        )

    if is_rate_limited(_client_ip(request)):
        return JsonResponse(
            {"error": "Has enviado muchas preguntas seguidas. Espera un minuto e inténtalo de nuevo."},
            status=429,
        )

    history = _clean_history(payload.get("history", []))
    try:
        reply = ask_gemini(message, history)
    except ChatbotError as exc:
        fallback = local_answer(message)
        if fallback:
            return JsonResponse({"reply": fallback, "source": "local"})
        return JsonResponse({"error": str(exc)}, status=503)
    return JsonResponse({"reply": reply})
