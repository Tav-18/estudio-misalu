from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import ContactMessageForm

CLASSES = [
    {"name": "Urbano", "slug": "urbano","image": "core/img/urbano.webp", "eyebrow": "Hip Hop · Street Dance · Freestyle",
     "description": "Una propuesta dinámica para desarrollar coordinación, musicalidad, confianza, actitud y un estilo propio.", "icon": "⚡"},
    {"name": "Contemporáneo", "slug": "contemporaneo","image": "core/img/contemporaneo.webp", "eyebrow": "Técnica · Fluidez · Expresión",
     "description": "Movimiento consciente para conectar técnica, creatividad, emociones y expresión corporal.", "icon": "✦"},
    {"name": "K-pop", "slug": "kpop","image": "core/img/kpop.webp", "eyebrow": "Coreografías · Precisión · Escena",
     "description": "Coreografías dinámicas con énfasis en coordinación, precisión, presencia escénica y trabajo en equipo.", "icon": "★"},
]

SCHEDULE = [
    {
        "class": "Urbano",
        "days": "Lun · Mié · Vie",
        "time": "17:00 – 18:30",
    },
    {
        "class": "Contemporáneo",
        "days": "Mar · Jue",
        "time": "18:30 – 20:00",
    },
    {
        "class": "K-pop",
        "days": "Sábado",
        "time": "11:00 – 12:30",
    },
]


GALLERY = [
    {
        "label": "Clase grupal",
        "image": "core/img/galeria-01.webp",
        "alt": "Grupo de bailarines en formación con iluminación morada",
        "caption": "Energía, coordinación y trabajo en equipo.",
        "css_class": "gallery-one",
    },
    {
        "label": "Entrenamiento",
        "image": "core/img/galeria-02.webp",
        "alt": "Bailarín realizando un movimiento de breakdance",
        "caption": "Técnica, movimiento y práctica.",
        "css_class": "gallery-two",
    },
    {
        "label": "Ensayo",
        "image": "core/img/galeria-03.webp",
        "alt": "Grupo de bailarines realizando un ensayo",
        "caption": "Aprendizaje, convivencia y preparación.",
        "css_class": "gallery-three",
    },
    {
        "label": "Presentaciones",
        "image": "core/img/galeria-04.webp",
        "alt": "Grupo de bailarines durante una presentación en escenario",
        "caption": "Experiencia escénica y shows.",
        "css_class": "gallery-four",
    },
]

VALUES = [
    {"title": "Creatividad y libertad de expresión", "text": "Impulsar la innovación artística y que cada estudiante explore su estilo propio sin miedo al fracaso.", "icon": "✦"},
    {"title": "Pasión y compromiso", "text": "Reflejar el amor por la danza junto con disciplina, rigor técnico y práctica constante.", "icon": "♥"},
    {"title": "Conexión humana y empatía", "text": "Usar el movimiento como lenguaje para expresar emociones y conectar con otras personas.", "icon": "◎"},
    {"title": "Colaboración y trabajo en equipo", "text": "Construir un espacio de apoyo mutuo, convivencia y aprendizaje compartido.", "icon": "◇"},
    {"title": "Accesibilidad y responsabilidad social", "text": "Acercar la danza a más personas y reducir barreras que dificultan el acceso a actividades artísticas.", "icon": "↗"},
    {"title": "Respeto hacia la diversidad", "text": "Valorar perspectivas culturales, de edad, género y pensamiento dentro del trabajo colectivo.", "icon": "∞"},
]

PESTEL = [
    {"letter": "P", "title": "Político", "text": "Los programas gubernamentales de apoyo a la cultura y al deporte pueden representar oportunidades; también influyen los cambios regulatorios para establecimientos y actividades recreativas."},
    {"letter": "E", "title": "Económico", "text": "La economía familiar puede afectar la capacidad de pago y la inflación puede elevar renta, servicios, mantenimiento y salarios."},
    {"letter": "S", "title": "Social", "text": "Existe interés entre jóvenes por K-pop, danza urbana y contemporánea, además de espacios de convivencia y expresión personal."},
    {"letter": "T", "title": "Tecnológico", "text": "Las redes sociales y plataformas digitales facilitan promoción, inscripciones, comunicación y difusión de horarios."},
    {"letter": "E", "title": "Ecológico", "text": "Se consideran medidas de ahorro de agua y electricidad, uso responsable de materiales, reducción de residuos y condiciones adecuadas de ventilación e iluminación."},
    {"letter": "L", "title": "Legal", "text": "La operación requiere cumplir obligaciones fiscales, laborales y de seguridad, además de medidas de protección para alumnos."},
]

DEMO_CONTACT = {
    "email": "hola@misalu.example",
    "phone": "+52 55 6480 9377",
    "address": "Alberto Braniff 202, Aviación Civil, Venustiano Carranza, 15740 Ciudad de México, CDMX",
}

def _common_context():
    return {"classes": CLASSES, "schedule": SCHEDULE, "values": VALUES, "gallery": GALLERY, "demo_contact": DEMO_CONTACT}

def home(request):
    form = ContactMessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "¡Gracias! una persona de nuestro equipo se contactara con usted.")
        return redirect("core:home")
    context = _common_context()
    context["form"] = form
    return render(request, "core/home.html", context)

def project_info(request):
    context = _common_context()
    context["pestel"] = PESTEL
    return render(request, "core/project_info.html", context)
