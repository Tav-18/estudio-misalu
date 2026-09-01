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
