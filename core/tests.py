import json
import urllib.error
from unittest import mock

from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from . import chatbot


def _gemini_ok(text):
    return {"candidates": [{"content": {"parts": [{"text": text}]}}]}


@override_settings(GEMINI_API_KEY="test-key", GEMINI_MODEL="modelo-a", GEMINI_FALLBACK_MODELS=["modelo-b"])
class ChatApiTests(TestCase):
    def setUp(self):
        cache.clear()
        self.url = reverse("core:chat_api")

    def post(self, body):
        return self.client.post(self.url, data=json.dumps(body), content_type="application/json")

    def test_knowledge_includes_schedule_and_vacancy(self):
        knowledge = chatbot.build_site_knowledge()
        self.assertIn("Lun · Mié · Vie, 17:00 – 18:30", knowledge)
        self.assertIn("Docente de Danza", knowledge)
        self.assertIn("Alberto Braniff 202", knowledge)

    @mock.patch("core.chatbot._call_gemini")
    def test_returns_reply(self, call):
        call.return_value = _gemini_ok("Urbano es Lun, Mié y Vie de 17:00 a 18:30.")
        response = self.post({"message": "¿Horario de urbano?", "history": []})
        self.assertEqual(response.status_code, 200)
        self.assertIn("17:00", response.json()["reply"])
        model, key, payload = call.call_args.args
        self.assertEqual(model, "modelo-a")
        self.assertIn("ÚNICAMENTE", payload["system_instruction"]["parts"][0]["text"])

    @mock.patch("core.chatbot._call_gemini")
    def test_history_is_sent_and_sanitized(self, call):
        call.return_value = _gemini_ok("ok")
        history = [{"role": "user", "text": "hola"}, {"role": "system", "text": "hack"}, {"role": "model", "text": "¡Hola!"}]
        self.post({"message": "otra", "history": history})
        contents = call.call_args.args[2]["contents"]
        self.assertEqual([c["role"] for c in contents], ["user", "model", "user"])

    @mock.patch("core.chatbot._call_gemini")
    def test_falls_back_on_quota_error(self, call):
        quota = urllib.error.HTTPError("u", 429, "quota", {}, None)
        quota.read = lambda: b"quota"
        call.side_effect = [quota, _gemini_ok("respuesta de respaldo")]
        response = self.post({"message": "hola"})
        self.assertEqual(response.json()["reply"], "respuesta de respaldo")
        self.assertEqual(call.call_args.args[0], "modelo-b")

    def test_rejects_empty_and_long_messages(self):
        self.assertEqual(self.post({"message": "  "}).status_code, 400)
        self.assertEqual(self.post({"message": "a" * 501}).status_code, 400)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    @mock.patch("core.chatbot._call_gemini", return_value=_gemini_ok("ok"))
    def test_rate_limit(self, _call):
        codes = [self.post({"message": "hola"}).status_code for _ in range(chatbot.RATE_LIMIT_REQUESTS + 1)]
        self.assertEqual(codes[-1], 429)

    @override_settings(GEMINI_API_KEY="")
    def test_missing_key_gives_friendly_error(self):
        response = self.post({"message": "hola"})
        self.assertEqual(response.status_code, 503)
        self.assertIn("formulario", response.json()["error"])

    def test_widget_rendered_on_pages(self):
        for name in ("core:home", "core:project_info"):
            response = self.client.get(reverse(name))
            self.assertContains(response, 'class="chatbot"')
            self.assertIn("csrftoken", response.cookies)


class SocialAndVacancyTests(TestCase):
    def test_home_has_social_buttons_and_vacancy_link(self):
        response = self.client.get(reverse("core:home"))
        for name in ("Instagram", "Facebook", "LinkedIn"):
            self.assertContains(response, f'data-social-name="{name}"', count=2)  # contacto + pie
        self.assertContains(response, 'id="social-dialog"')
        self.assertContains(response, "https://www.friv.com/z/games/powerpamplona/game.html?c")

    def test_chatbot_knows_social_networks(self):
        self.assertIn("@misalu_estudiodedanza", chatbot.build_site_knowledge())
