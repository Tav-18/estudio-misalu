import json
import urllib.error
from unittest import mock

from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from . import chatbot
from .models import Worker


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
        self.assertContains(response, "https://www.friv.com/z/games/powerpamplona/game.html?c", count=2)  # menú + sección
        self.assertContains(response, 'data-scroll-target="#vacante"')
        self.assertContains(response, 'id="vacante"')

    def test_chatbot_knows_social_networks(self):
        self.assertIn("@misalu_estudiodedanza", chatbot.build_site_knowledge())


@override_settings(GEMINI_API_KEY="test-key", GEMINI_MODEL="modelo-a", GEMINI_FALLBACK_MODELS=["modelo-b"])
class ResilienceTests(TestCase):
    def setUp(self):
        cache.clear()
        self.url = reverse("core:chat_api")

    def post(self, message):
        return self.client.post(self.url, data=json.dumps({"message": message}), content_type="application/json")

    @staticmethod
    def _http_error(code):
        error = urllib.error.HTTPError("u", code, "err", {}, None)
        error.read = lambda: b"err"
        return error

    @mock.patch("core.chatbot.time.sleep")
    @mock.patch("core.chatbot._call_gemini")
    def test_retries_same_model_when_busy(self, call, _sleep):
        call.side_effect = [self._http_error(503), _gemini_ok("segundo intento")]
        response = self.post("hola")
        self.assertEqual(response.json()["reply"], "segundo intento")
        self.assertEqual([c.args[0] for c in call.call_args_list], ["modelo-a", "modelo-a"])

    @mock.patch("core.chatbot.time.sleep")
    @mock.patch("core.chatbot._call_gemini")
    def test_local_answer_when_gemini_down(self, call, _sleep):
        call.side_effect = self._http_error(503)
        response = self.post("¿Qué horarios tienen?")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["source"], "local")
        self.assertIn("17:00 – 18:30", response.json()["reply"])
        self.assertEqual(call.call_count, 4)  # 2 modelos x 2 intentos

    @mock.patch("core.chatbot.time.sleep")
    @mock.patch("core.chatbot._call_gemini")
    def test_unknown_question_still_errors_when_gemini_down(self, call, _sleep):
        call.side_effect = self._http_error(503)
        self.assertEqual(self.post("cuéntame un chiste").status_code, 503)

    def test_menu_questions_have_local_answers(self):
        menu = ["¿Qué clases ofrecen?", "¿Qué horarios tienen?", "¿Hay alguna vacante?",
                "¿Dónde están?", "¿Cómo los contacto?", "¿Quiénes son?"]
        expected = ["Urbano", "17:00", "Docente de Danza", "Alberto Braniff", "WhatsApp", "Alondra"]
        for question, text in zip(menu, expected):
            self.assertIn(text, chatbot.local_answer(question), question)


class InternalAreaTests(TestCase):
    def setUp(self):
        self.url = reverse("core:internal_area")

    def login(self, email, password):
        return self.client.post(reverse("core:internal_login"), {"email": email, "password": password})

    def visible_names(self, response):
        return [w["nombre"] for w in response.context["workers"] if w["visible"]]

    def test_requires_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('core:internal_login')}?next={self.url}")

    def test_login_page_does_not_show_credentials(self):
        response = self.client.get(reverse("core:internal_login"))
        self.assertContains(response, "Perfiles de acceso")
        for word in ("RH2026", "Admin2026", "Misalu2026", "prueba", "ficticio", "demostración"):
            self.assertNotContains(response, word)

    def test_wrong_password_is_rejected(self):
        response = self.login("rh@estudiomisalu.mx", "incorrecta")
        self.assertContains(response, "Correo o contraseña incorrectos")
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_home_menu_links_to_internal_area(self):
        self.assertContains(self.client.get(reverse("core:home")), self.url)

    def test_worker_account_sees_workers_but_rh_is_locked(self):
        self.login("personal@estudiomisalu.mx", "Misalu2026")
        response = self.client.get(self.url, {"tab": "rh"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["workers"]), 25)
        self.assertContains(response, "Contenido exclusivo de Recursos Humanos")
        self.assertNotContains(response, "rh-analisis-puesto")
        self.assertNotContains(response, "Agregar trabajador")
        self.assertEqual(self.client.get(reverse("core:worker_create")).status_code, 302)
        self.assertContains(response, "vacante-docente")

    def test_rh_account_sees_campaign_video_and_image(self):
        self.login("rh@estudiomisalu.mx", "RH2026")
        response = self.client.get(self.url, {"tab": "rh"})
        self.assertEqual(response.context["active_tab"], "rh")
        self.assertContains(response, "rh-analisis-puesto")
        self.assertContains(response, "analisis-puesto")
        self.assertContains(response, "Evaluación del desempeño")
        self.assertNotContains(response, "Agregar trabajador")

    def test_filters_combine(self):
        self.login("rh@estudiomisalu.mx", "RH2026")
        response = self.client.get(self.url, {"puesto": "Docente", "disciplina": "K-pop", "estatus": "Activo"})
        self.assertEqual(sorted(self.visible_names(response)), ["Camila Vargas", "José Luis Morales"])

    def test_search_ignores_accents_and_case(self):
        self.login("personal@estudiomisalu.mx", "Misalu2026")
        response = self.client.get(self.url, {"q": "jose luis"})
        self.assertEqual(self.visible_names(response), ["José Luis Morales"])

    def test_admin_can_add_edit_and_delete_workers(self):
        self.login("ADMIN@estudiomisalu.mx", "Admin2026")
        self.assertContains(self.client.get(self.url), "Agregar trabajador")
        data = {"nombre": "Lucía Pérez", "cargo": "Maestra de urbano", "puesto": "Docente", "area": "Académica",
                "disciplina": "Urbano", "tipo": "Medio tiempo", "estatus": "Activo", "ingreso": 2026}
        self.client.post(reverse("core:worker_create"), data)
        worker = Worker.objects.get(nombre="Lucía Pérez")
        self.client.post(reverse("core:worker_edit", args=[worker.pk]), {**data, "estatus": "Inactivo"})
        worker.refresh_from_db()
        self.assertEqual(worker.estatus, "Inactivo")
        self.client.post(reverse("core:worker_delete", args=[worker.pk]))
        self.assertFalse(Worker.objects.filter(pk=worker.pk).exists())

    def test_logout(self):
        self.login("rh@estudiomisalu.mx", "RH2026")
        self.client.post(reverse("core:internal_logout"))
        self.assertEqual(self.client.get(self.url).status_code, 302)



class RhDocumentsTests(TestCase):
    """Expedientes de candidatos y Manual de políticas en la pestaña de Recursos Humanos."""

    def setUp(self):
        import shutil
        import tempfile
        from pathlib import Path

        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        ana = self.tmp / "expedientes" / "Ana López"
        for folder in ("1 Documentos de ingreso", "2 Pruebas psicométricas", "3 Pruebas proyectivas", "4 Reportes"):
            (ana / folder).mkdir(parents=True)
        (ana / "1 Documentos de ingreso" / "Solicitud de empleo - Ana López.pdf").write_bytes(b"%PDF sol")
        (ana / "1 Documentos de ingreso" / "Currículum vitae - Ana López.pdf").write_bytes(b"%PDF cv")
        (ana / "2 Pruebas psicométricas" / "Cleaver - Ana López.pdf").write_bytes(b"%PDF-1.4 prueba")
        (ana / "2 Pruebas psicométricas" / "Cleaver - Ana López.docx").write_bytes(b"docx")
        (ana / "3 Pruebas proyectivas" / "Machover - Ana López.pdf").write_bytes(b"%PDF")
        (ana / "4 Reportes" / "Reporte mixto - Ana López.pdf").write_bytes(b"%PDF")
        (ana / "notas.exe").write_bytes(b"no permitido")
        beto = self.tmp / "expedientes" / "Beto Ruiz"
        beto.mkdir()
        (beto / "Suelto.pdf").write_bytes(b"%PDF")
        manual = self.tmp / "expedientes" / "Manual"
        manual.mkdir()
        (manual / "Manual de políticas.pdf").write_bytes(b"%PDF-1.4 manual")
        (manual / "Manual de políticas.docx").write_bytes(b"docx")
        (self.tmp / "secreto.txt").write_text("fuera")
        self.settings_override = override_settings(RH_DOCUMENTS_DIR=self.tmp)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)

    def login(self, email, password):
        self.client.post(reverse("core:internal_login"), {"email": email, "password": password})

    def doc_url(self, path):
        return reverse("core:rh_document", args=[path])

    def rh_page(self, extra=""):
        return self.client.get(reverse("core:internal_area") + "?tab=rh" + extra)

    def test_expedientes_have_ordered_categories_and_paired_originals(self):
        self.login("rh@estudiomisalu.mx", "RH2026")
        exps = self.rh_page().context["expedientes"]
        self.assertEqual([e["name"] for e in exps], ["Ana López", "Beto Ruiz"])  # "Manual" no es expediente
        ana = exps[0]
        self.assertEqual([c["name"] for c in ana["categories"]],
                         ["Documentos de ingreso", "Pruebas psicométricas", "Pruebas proyectivas", "Reportes"])
        cleaver = ana["categories"][1]["files"][0]
        self.assertEqual(cleaver["name"], "Cleaver")
        self.assertEqual(cleaver["ext"], "pdf")
        self.assertEqual(cleaver["original"]["ext"], "docx")
        self.assertEqual(ana["total"], 5)  # el .exe no cuenta y el Word va junto a su PDF

    def test_summary_counts_documents(self):
        self.login("rh@estudiomisalu.mx", "RH2026")
        response = self.rh_page()
        ana, beto = response.context["expedientes"]
        self.assertEqual(len(ana["categories"]), 4)
        self.assertEqual(beto["categories"][0]["name"], "Otros documentos")
        summary = response.context["expedientes_summary"]
        self.assertEqual((summary["count"], summary["documents"]), (2, 6))
        self.assertContains(response, "Expedientes de candidatos")
        self.assertNotContains(response, "En proceso")

    def test_selected_expediente_from_query(self):
        self.login("rh@estudiomisalu.mx", "RH2026")
        self.assertEqual(self.rh_page().context["selected_exp"], "ana-lopez")
        self.assertEqual(self.rh_page("&exp=beto-ruiz").context["selected_exp"], "beto-ruiz")
        self.assertEqual(self.rh_page("&exp=no-existe").context["selected_exp"], "ana-lopez")

    def test_manual_card(self):
        self.login("admin@estudiomisalu.mx", "Admin2026")
        response = self.rh_page()
        manual = response.context["manual_docs"]
        self.assertEqual(len(manual), 1)
        self.assertEqual(manual[0]["original"]["ext"], "docx")
        self.assertContains(response, "RH-MP-001")
        self.assertContains(response, "Consultar manual")

    def test_rh_can_open_and_download_documents(self):
        self.login("rh@estudiomisalu.mx", "RH2026")
        path = "expedientes/Ana López/2 Pruebas psicométricas/Cleaver - Ana López.pdf"
        response = self.client.get(self.doc_url(path))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn("inline", response["Content-Disposition"])
        self.assertEqual(b"".join(response.streaming_content), b"%PDF-1.4 prueba")
        download = self.client.get(self.doc_url("expedientes/Manual/Manual de políticas.docx") + "?descargar=1")
        self.assertIn("attachment", download["Content-Disposition"])

    def test_personal_account_cannot_see_or_open_documents(self):
        self.login("personal@estudiomisalu.mx", "Misalu2026")
        response = self.rh_page()
        self.assertEqual(response.context["expedientes"], [])
        self.assertNotContains(response, "Cleaver")
        doc = self.client.get(self.doc_url("expedientes/Manual/Manual de políticas.pdf"))
        self.assertNotEqual(doc.status_code, 200)

    def test_anonymous_cannot_open_documents(self):
        doc = self.client.get(self.doc_url("expedientes/Manual/Manual de políticas.pdf"))
        self.assertEqual(doc.status_code, 302)

    def test_blocks_paths_outside_folder_and_disallowed_types(self):
        self.login("admin@estudiomisalu.mx", "Admin2026")
        self.assertEqual(self.client.get(self.doc_url("../config/settings.py")).status_code, 404)
        self.assertEqual(self.client.get(self.doc_url("secreto.txt")).status_code, 404)
        self.assertEqual(self.client.get(self.doc_url("expedientes/Ana López/notas.exe")).status_code, 404)
