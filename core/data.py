"""Contenido del sitio compartido por las vistas y el chatbot."""

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
    "email": "contacto@estudiomisalu.mx",
    "phone": "+52 55 6480 9377",
    "address": "Alberto Braniff 202, Aviación Civil, Venustiano Carranza, 15740 Ciudad de México, CDMX",
}


# Redes sociales simuladas: al hacer clic se muestra una captura del perfil (no hay páginas reales).
SOCIAL_NETWORKS = [
    {
        "slug": "instagram",
        "name": "Instagram",
        "handle": "@misalu_estudiodedanza",
        "url": "instagram.com/misalu_estudiodedanza",
        "image": "core/img/social/instagram.jpg",
    },
    {
        "slug": "facebook",
        "name": "Facebook",
        "handle": "MISALÚ | Estudio de Danza",
        "url": "facebook.com/misalu.estudiodedanza",
        "image": "core/img/social/facebook.jpg",
    },
    {
        "slug": "linkedin",
        "name": "LinkedIn",
        "handle": "MISALÚ | Estudio de Danza",
        "url": "linkedin.com/company/misalu-estudio-de-danza",
        "image": "core/img/social/linkedin.jpg",
    },
]

# Enlace del botón "Ver vacante".
VACANCY_URL = "https://www.friv.com/z/games/powerpamplona/game.html?c"


# ===== Área interna =====
# Opciones de los filtros de "Trabajadores". El orden aquí es el orden en que aparecen.
WORKER_FILTERS = [
    {"key": "puesto", "label": "Puesto",
     "options": ["Dirección", "Docente", "Administración", "Marketing", "Recursos Humanos", "Recepción", "Servicios"]},
    {"key": "area", "label": "Área",
     "options": ["Dirección general", "Académica", "Administración", "Marketing", "Recursos Humanos", "Servicios"]},
    {"key": "disciplina", "label": "Disciplina",
     "options": ["Urbano", "K-pop", "Contemporáneo"]},
    {"key": "tipo", "label": "Tipo de trabajador",
     "options": ["Tiempo completo", "Medio tiempo"]},
    {"key": "estatus", "label": "Estatus",
     "options": ["Activo", "Inactivo"]},
]

# Personal inicial de Misalú (coincide con el Directorio, más dos bajas).
# Se carga a la base de datos con la migración 0002; después se edita desde el Área interna (cuenta admin).
WORKERS = [
    {"nombre": "Sara Romero", "cargo": "Directora general", "puesto": "Dirección", "area": "Dirección general", "disciplina": "", "tipo": "Tiempo completo", "estatus": "Activo", "ingreso": "2023"},
    {"nombre": "Nancy Rodríguez", "cargo": "Fundadora", "puesto": "Dirección", "area": "Dirección general", "disciplina": "", "tipo": "Tiempo completo", "estatus": "Activo", "ingreso": "2023"},
    {"nombre": "Alondra Laguna", "cargo": "Fundadora", "puesto": "Dirección", "area": "Dirección general", "disciplina": "", "tipo": "Tiempo completo", "estatus": "Activo", "ingreso": "2023"},
    {"nombre": "Iván Bello", "cargo": "Fundador", "puesto": "Dirección", "area": "Dirección general", "disciplina": "", "tipo": "Tiempo completo", "estatus": "Activo", "ingreso": "2023"},
    {"nombre": "Valeria Martínez", "cargo": "Directora académica", "puesto": "Dirección", "area": "Académica", "disciplina": "", "tipo": "Tiempo completo", "estatus": "Activo", "ingreso": "2023"},
    {"nombre": "Alejandro García", "cargo": "Maestro de urbano", "puesto": "Docente", "area": "Académica", "disciplina": "Urbano", "tipo": "Medio tiempo", "estatus": "Activo", "ingreso": "2024"},
    {"nombre": "Daniela Sánchez", "cargo": "Maestra de urbano", "puesto": "Docente", "area": "Académica", "disciplina": "Urbano", "tipo": "Tiempo completo", "estatus": "Activo", "ingreso": "2023"},
    {"nombre": "José Luis Morales", "cargo": "Maestro de K-pop", "puesto": "Docente", "area": "Académica", "disciplina": "K-pop", "tipo": "Medio tiempo", "estatus": "Activo", "ingreso": "2024"},
    {"nombre": "Camila Vargas", "cargo": "Maestra de K-pop", "puesto": "Docente", "area": "Académica", "disciplina": "K-pop", "tipo": "Medio tiempo", "estatus": "Activo", "ingreso": "2025"},
    {"nombre": "Roberto Flores", "cargo": "Maestro de contemporáneo", "puesto": "Docente", "area": "Académica", "disciplina": "Contemporáneo", "tipo": "Tiempo completo", "estatus": "Activo", "ingreso": "2023"},
    {"nombre": "Andrea Castillo", "cargo": "Maestra de contemporáneo", "puesto": "Docente", "area": "Académica", "disciplina": "Contemporáneo", "tipo": "Medio tiempo", "estatus": "Activo", "ingreso": "2024"},
    {"nombre": "Fernanda Ruiz", "cargo": "Maestra de K-pop", "puesto": "Docente", "area": "Académica", "disciplina": "K-pop", "tipo": "Medio tiempo", "estatus": "Inactivo", "ingreso": "2023"},
    {"nombre": "Miguel Ángel Cruz", "cargo": "Director administrativo", "puesto": "Dirección", "area": "Administración", "disciplina": "", "tipo": "Tiempo completo", "estatus": "Activo", "ingreso": "2023"},
    {"nombre": "Sofía Mendoza", "cargo": "Tesorera", "puesto": "Administración", "area": "Administración", "disciplina": "", "tipo": "Tiempo completo", "estatus": "Activo", "ingreso": "2023"},
    {"nombre": "Luis Fernando Ortiz", "cargo": "Contabilidad", "puesto": "Administración", "area": "Administración", "disciplina": "", "tipo": "Medio tiempo", "estatus": "Activo", "ingreso": "2024"},
    {"nombre": "Paola Jiménez", "cargo": "Directora de marketing", "puesto": "Dirección", "area": "Marketing", "disciplina": "", "tipo": "Tiempo completo", "estatus": "Activo", "ingreso": "2023"},
    {"nombre": "Ricardo Navarro", "cargo": "Community manager", "puesto": "Marketing", "area": "Marketing", "disciplina": "", "tipo": "Medio tiempo", "estatus": "Activo", "ingreso": "2024"},
    {"nombre": "Karen Flores", "cargo": "Diseño y publicidad", "puesto": "Marketing", "area": "Marketing", "disciplina": "", "tipo": "Medio tiempo", "estatus": "Activo", "ingreso": "2024"},
    {"nombre": "Emmanuel Reyes", "cargo": "Eventos y presentaciones", "puesto": "Marketing", "area": "Marketing", "disciplina": "", "tipo": "Medio tiempo", "estatus": "Activo", "ingreso": "2025"},
    {"nombre": "Diego Hernández", "cargo": "Recursos Humanos", "puesto": "Recursos Humanos", "area": "Recursos Humanos", "disciplina": "", "tipo": "Tiempo completo", "estatus": "Activo", "ingreso": "2023"},
    {"nombre": "Natalia Cruz", "cargo": "Directora de servicios", "puesto": "Dirección", "area": "Servicios", "disciplina": "", "tipo": "Tiempo completo", "estatus": "Activo", "ingreso": "2023"},
    {"nombre": "Gabriela Torres", "cargo": "Recepción", "puesto": "Recepción", "area": "Servicios", "disciplina": "", "tipo": "Tiempo completo", "estatus": "Activo", "ingreso": "2024"},
    {"nombre": "Héctor Aguilar", "cargo": "Recepción (turno tarde)", "puesto": "Recepción", "area": "Servicios", "disciplina": "", "tipo": "Medio tiempo", "estatus": "Inactivo", "ingreso": "2024"},
    {"nombre": "Jorge Ramírez", "cargo": "Limpieza", "puesto": "Servicios", "area": "Servicios", "disciplina": "", "tipo": "Medio tiempo", "estatus": "Activo", "ingreso": "2024"},
    {"nombre": "Daniela Vargas", "cargo": "Mantenimiento", "puesto": "Servicios", "area": "Servicios", "disciplina": "", "tipo": "Medio tiempo", "estatus": "Activo", "ingreso": "2025"},
]

# Procesos de Recursos Humanos (pestaña "Recursos Humanos").
HR_PROCESSES = [
    {"slug": "reclutamiento", "title": "Reclutamiento y selección", "icon": "◎",
     "summary": "Atraer y elegir a las personas adecuadas para cada puesto, con criterios claros y un proceso justo.",
     "steps": ["Requisición de personal", "Publicación de la vacante", "Filtro de CV", "Entrevista por competencias",
               "Clase muestra / prueba práctica", "Pruebas psicométricas", "Oferta y contratación"],
     "note": "Proceso en curso: Docente de Danza · 14 postulaciones · 5 en entrevista · 2 en clase muestra."},
    {"slug": "analisis", "title": "Análisis de puestos", "icon": "◇",
     "summary": "Describir qué hace cada puesto, qué se necesita para ocuparlo y cómo se relaciona con los demás.",
     "rows": [
         ("Puesto", "Docente de Danza"),
         ("Reporta a", "Dirección académica"),
         ("Objetivo", "Impartir clases por niveles y acompañar el desarrollo técnico y expresivo de los alumnos."),
         ("Funciones", "Planear clases, montar coreografías, evaluar el avance y preparar presentaciones."),
         ("Perfil", "Experiencia docente en danza; dominio de urbano, K-pop o contemporáneo."),
         ("Competencias", "Comunicación, empatía, trabajo en equipo, creatividad y puntualidad."),
     ]},
    {"slug": "desempeno", "title": "Evaluación del desempeño", "icon": "↗",
     "summary": "Medir cada semestre cómo trabaja cada persona para reconocer logros y detectar áreas de mejora.",
     "criteria": [("Calidad de las clases", 30), ("Puntualidad y asistencia", 20),
                  ("Trabajo en equipo", 20), ("Satisfacción de alumnos", 20), ("Iniciativa", 10)],
     "note": "Método: escala de 1 a 5 + retroalimentación 360° (dirección, compañeros y alumnos)."},
    {"slug": "capacitacion", "title": "Capacitación", "icon": "✦",
     "summary": "Plan anual para actualizar técnicas, pedagogía y habilidades de atención al alumno.",
     "courses": [("Primeros auxilios y prevención de lesiones", "Todo el personal", "Febrero"),
               ("Didáctica de la danza por niveles", "Docentes", "Abril"),
               ("Atención y servicio al cliente", "Recepción y servicios", "Junio"),
               ("Inclusión y trato respetuoso", "Todo el personal", "Septiembre")]},
    {"slug": "expedientes", "title": "Expedientes", "icon": "▤",
     "summary": "Cada trabajador cuenta con un expediente digital con la documentación necesaria para su contratación.",
     "checklist": ["Solicitud de empleo y CV", "Contrato firmado", "Comprobante de domicilio",
                   "Comprobante de estudios", "Alta en el IMSS", "Evaluaciones de desempeño"]},
    {"slug": "vacantes", "title": "Vacantes", "icon": "★",
     "summary": "Puestos abiertos actualmente en Misalú.",
     "vacancies": [("Docente de Danza", "Dirección académica", "Medio tiempo")]},
    {"slug": "personal", "title": "Personal", "icon": "♥",
     "summary": "Indicadores generales de la plantilla, calculados a partir de la tabla de trabajadores."},
]

# ===== Acceso al Área interna =====
# Cuentas institucionales por perfil. Las contraseñas se entregan al personal; no se muestran en el sitio.
# Cada rol define qué puede ver o hacer la persona dentro del portal.
INTERNAL_ROLES = {
    "trabajador": {"label": "Personal", "can_view_rh": False, "can_edit": False,
                   "description": "Consulta del directorio de trabajadores."},
    "rh": {"label": "Recursos Humanos", "can_view_rh": True, "can_edit": False,
           "description": "Directorio de trabajadores, procesos de Recursos Humanos y comunicados al equipo."},
    "admin": {"label": "Administración", "can_view_rh": True, "can_edit": True,
              "description": "Acceso completo, incluida la gestión del personal (altas, cambios y bajas)."},
}

DEMO_ACCOUNTS = [
    {"email": "personal@estudiomisalu.mx", "password": "Misalu2026", "role": "trabajador", "name": "Equipo Misalú"},
    {"email": "rh@estudiomisalu.mx", "password": "RH2026", "role": "rh", "name": "Diego Hernández"},
    {"email": "admin@estudiomisalu.mx", "password": "Admin2026", "role": "admin", "name": "Sara Romero"},
]

# Ficha del Manual de políticas que se muestra en la pestaña "Recursos Humanos".
# El archivo en sí está en documentos_rh/manual/.
HR_MANUAL = {
    "title": "Manual de Políticas y Procedimientos",
    "subtitle": "Reclutamiento y selección de personal",
    "summary": ("Establece las políticas y los procedimientos estandarizados para cubrir las vacantes del estudio "
                "con base en el perfil del puesto, las competencias requeridas y criterios objetivos."),
    "facts": [("Código", "RH-MP-001"), ("Versión", "1.0"), ("Área", "Recursos Humanos / Capital Humano"),
              ("Emisión", "15/11/2026"), ("Vigencia", "15/11/2027")],
    "people": [("Elaboró", "Alondra Laguna y Nancy Rodríguez"), ("Revisó", "Iván Bello"), ("Autorizó", "Sara Romero")],
    "contents": ["Objetivo", "Alcance", "Marco normativo", "Definiciones", "Responsabilidades por área",
                 "Políticas generales", "Procedimiento de reclutamiento y selección",
                 "Procedimiento de contratación e ingreso", "Diagrama general del proceso",
                 "Registros y control documental", "Confidencialidad y protección de datos",
                 "Revisión y actualización del manual"],
}

# Material de la campaña de RH que se muestra en la pestaña "Recursos Humanos".
HR_CAMPAIGN = {
    "title": "Seguimos creciendo juntos",
    "subtitle": "Comunicado al equipo sobre el análisis de puesto",
    "text": ("Este proceso nos permitirá conocer y evaluar cada puesto de trabajo para mejorar la organización "
             "y la experiencia de todo el equipo. El enfoque está en el puesto, no en la persona: no implica "
             "evaluar tu desempeño ni pone en riesgo tu puesto."),
    "tools": ["Entrevistas con el equipo", "Cuestionarios sobre las actividades", "Observación directa del día a día"],
    "image": "core/img/rh/analisis-puesto.jpg",
    "video": "core/media/rh-analisis-puesto.mp4",
    "video_webm": "core/media/rh-analisis-puesto.webm",  # respaldo para navegadores sin MP4/H.264
    "poster": "core/media/rh-analisis-puesto-poster.jpg",
}

# Anuncio de vacante que se muestra en la pestaña "Trabajadores" (visible para todos los perfiles).
VACANCY_CAMPAIGN = {
    "kicker": "Vacante por proyecto",
    "title": "Docente de Danza",
    "text": ("Buscamos a un o una docente para impartir clases y participar en la formación de nuestros alumnos. "
             "Si conoces a alguien con el perfil, compártele la vacante: ¡únete al equipo!"),
    "chips": ["Programas de entrenamiento", "Clases por niveles", "Coreografías"],
    "area": "Dirección académica",
    "video": "core/media/vacante-docente.mp4",
    "video_webm": "core/media/vacante-docente.webm",
    "poster": "core/media/vacante-docente-poster.jpg",
}
