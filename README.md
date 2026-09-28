# Estudio de Danza Misalú

Sitio web académico desarrollado con Python + Django.

## Funcionalidades incluidas

- Landing page responsive.
- Navegación móvil accesible.
- Secciones Inicio, Nosotros, Clases, Horarios, Galería y Contacto.
- Formulario de contacto funcional.
- Los mensajes quedan almacenados en SQLite y se pueden consultar desde Django Admin.
- Galería interactiva con diálogo.
- Animaciones suaves respetando `prefers-reduced-motion`.
- Estados de foco para navegación por teclado.
- Diseño basado en la identidad visual del logo: cian, turquesa, morado, magenta y rosa.
- WhiteNoise y Gunicorn preparados para despliegue.

## Estructura

```text
misalu_django/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── core/
│   ├── migrations/
│   ├── static/core/
│   │   ├── css/styles.css
│   │   ├── js/main.js
│   │   └── img/logo-misalu.png
│   ├── templates/core/
│   │   ├── base.html
│   │   └── home.html
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
├── Procfile
├── render.yaml
└── .env.example
```

## Ejecutar en Windows PowerShell

Desde la carpeta del proyecto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abrir:

```text
http://127.0.0.1:8000/
```

Panel administrativo:

```text
http://127.0.0.1:8000/admin/
```

## Antes de publicar

1. Copia `.env.example` como referencia y configura variables reales en el hosting.
2. Usa `DJANGO_DEBUG=False`.
3. Define el dominio en `DJANGO_ALLOWED_HOSTS`.
4. Define HTTPS en `CSRF_TRUSTED_ORIGINS`.
5. Sustituye correo, WhatsApp, dirección y horarios de ejemplo.
6. Sustituye la galería abstracta por fotos reales y optimizadas en WebP/AVIF.
7. Agrega favicon y metadatos Open Graph cuando estén disponibles.

## Siguiente fase recomendada

- Revisar el diseño ejecutándolo en computadora y móvil.
- Sustituir textos/datos provisionales.
- Añadir imágenes reales.
- Configurar dominio.
- Desplegar en un servicio compatible con Django.


## Versión 2
Incluye Quiénes somos, historia, misión, visión, valores, Core Business, organigrama HTML/CSS, vacante, espacio para directorio, datos de contacto ficticios, guía de imágenes y página `/proyecto/` con S.A.S., Know How y PESTEL.


## Chatbot con Google Gemini (versión 3)

El sitio incluye un asistente virtual (botón flotante abajo a la derecha) que **solo responde sobre
Misalú**: clases, horarios, vacante, equipo, organigrama, contacto, misión/visión, PESTEL, etc.
Si le preguntan otra cosa, indica amablemente que solo puede ayudar con información del estudio.

### Cómo funciona

- `core/data.py`: contenido del sitio (clases, horarios, valores, contacto…). Lo usan la página y el chatbot.
- `core/chatbot.py`: arma el contexto del sitio, las reglas del asistente y llama a la API de Gemini.
  Si cambias textos de `home.html` (historia, vacante, directorio), actualiza también `STATIC_KNOWLEDGE` aquí.
- `core/views.py` → `chat_api`: endpoint `POST /api/chat/` (valida longitud, limita 12 mensajes/min por IP).
- `core/templates/core/_chatbot.html`, `core/static/core/js/chatbot.js` y el final de `styles.css`: el widget.
- La clave de Gemini **nunca** llega al navegador; solo la usa el servidor.

### Configuración

1. Crea una clave gratuita en <https://aistudio.google.com/apikey> (cuenta de Google, sin tarjeta).
2. Copia `.env.example` como `.env` y pega la clave:

   ```text
   GEMINI_API_KEY=tu-clave-aqui
   ```

3. Instala dependencias (se agregó `python-dotenv`) y ejecuta:

   ```powershell
   pip install -r requirements.txt
   python manage.py runserver
   ```

4. En Render: *Environment* → agrega `GEMINI_API_KEY` con tu clave (ya está declarada en `render.yaml`).

Modelo por defecto: `gemini-3.5-flash-lite` (rápido); si falla o se agota la cuota usa `gemini-3.6-flash`.
Se pueden cambiar con `GEMINI_MODEL` y `GEMINI_FALLBACK_MODELS`.

### Pruebas

```powershell
python manage.py test core
```


## Área interna (versión 4)

Nueva página `/area-interna/` (enlace **Área interna** en el menú) con dos pestañas:

- **Trabajadores**: tabla del personal con buscador (ignora acentos) y filtros por puesto, área,
  disciplina, tipo de trabajador y estatus. Se actualiza al instante; sin JavaScript también funciona
  con el botón "Aplicar filtros". En celular la tabla se muestra como tarjetas.
- **Recursos Humanos**: reclutamiento y selección, análisis de puestos, evaluación del desempeño,
  capacitación, expedientes, vacantes y personal (indicadores calculados desde la tabla).

Los datos están en `core/data.py` (`WORKERS`, `WORKER_FILTERS`, `HR_PROCESSES`); para agregar o cambiar
un trabajador solo edita esa lista. Archivos: `core/templates/core/internal_area.html`,
`core/static/core/js/internal.js` y el bloque "Área interna" al final de `styles.css`.

### Acceso al Área interna (versión 5)

Al entrar a **Área interna** se pide iniciar sesión. Las cuentas **no** se muestran en el sitio; se
entregan al personal:

| Correo | Contraseña | Perfil |
|---|---|---|
| `personal@estudiomisalu.mx` | `Misalu2026` | Personal: consulta el directorio de trabajadores. RH aparece bloqueado. |
| `rh@estudiomisalu.mx` | `RH2026` | Recursos Humanos: trabajadores, procesos de RH, video y cartel del análisis de puesto. |
| `admin@estudiomisalu.mx` | `Admin2026` | Administración: todo lo anterior + altas, cambios y bajas de trabajadores. |

- Las cuentas y los permisos por perfil están en `core/data.py` (`DEMO_ACCOUNTS`, `INTERNAL_ROLES`).
- Los trabajadores viven en la base de datos (modelo `Worker`). **Después de actualizar, ejecuta
  `python manage.py migrate`**: la migración `0002_worker` crea la tabla y carga al personal inicial.
- Video y cartel de RH: `core/static/core/media/` y `core/static/core/img/rh/` (configurados en `HR_CAMPAIGN`).
- Video de la vacante Docente de Danza en la pestaña Trabajadores (visible para todos los perfiles): `VACANCY_CAMPAIGN`.
- Las contraseñas están escritas en el código: sirve para presentar el portal, no para proteger información real.
- En Render (plan gratuito) la base SQLite se reinicia en cada despliegue: los cambios hechos con la cuenta
  admin se pierden y vuelve la lista inicial.
