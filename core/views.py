import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .chatbot import ChatbotError, ask_gemini, is_rate_limited
from .data import (
    CLASSES, DEMO_CONTACT, GALLERY, PESTEL, SCHEDULE, SOCIAL_NETWORKS, VACANCY_URL, VALUES,
)
from .forms import ContactMessageForm

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
        return JsonResponse({"error": str(exc)}, status=503)
    return JsonResponse({"reply": reply})
