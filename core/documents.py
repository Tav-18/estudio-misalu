"""Documentos de Recursos Humanos: expedientes de candidatos y manual de políticas.

Los archivos viven en ``documentos_rh/`` (fuera de ``static``) para que solo se puedan abrir con
una sesión de RH o Administración. Estructura:

    documentos_rh/
        expedientes/
            Nombre/
                1 Documentos de ingreso/      ← cada subcarpeta es una categoría;
                    Solicitud de empleo - Nombre.pdf   el número inicial solo define el orden
                    Solicitud de empleo - Nombre.docx  (mismo nombre = original del PDF)
                2 Pruebas psicométricas/
                3 Pruebas proyectivas/
                4 Reportes/
                archivo.pdf                    ← los sueltos van a "Otros documentos"
        manual/
            Manual ....pdf (+ .docx original opcional)

El texto antes de " - " es el título que se muestra (p. ej. "Cleaver - Dylan.pdf" → "Cleaver").
Basta con copiar las carpetas: la página las lista sola, sin tocar código.
"""
import re
import unicodedata
from pathlib import Path

from django.conf import settings

ALLOWED_EXTENSIONS = {
    ".pdf": "PDF", ".png": "Imagen", ".jpg": "Imagen", ".jpeg": "Imagen", ".webp": "Imagen",
    ".doc": "Word", ".docx": "Word", ".xls": "Excel", ".xlsx": "Excel", ".ppt": "PowerPoint",
    ".pptx": "PowerPoint", ".mp4": "Video",
}
# Tipos que el navegador puede mostrar en una pestaña; el resto se descarga.
INLINE_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".mp4"}
# Si existe un PDF y un archivo con el mismo nombre, el PDF es el principal y el otro el "original".
PREFERRED_ORDER = [".pdf", ".png", ".jpg", ".jpeg", ".webp", ".mp4", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt"]

MANUAL_FOLDER = "manual"
LOOSE_CATEGORY = "Otros documentos"

# Icono y descripción de cada categoría conocida (por nombre de carpeta sin el número).
CATEGORY_INFO = {
    "documentos de ingreso": ("🗂", "Solicitud de empleo y currículum"),
    "pruebas psicométricas": ("📊", "Inteligencia, personalidad, valores e intereses"),
    "pruebas proyectivas": ("✎", "Pruebas gráficas de personalidad"),
    "reportes": ("📝", "Integración de resultados"),
}

_CATEGORY_INFO = {}  # se llena al final con las claves sin acentos


def documents_root():
    return Path(getattr(settings, "RH_DOCUMENTS_DIR", settings.BASE_DIR / "documentos_rh")).resolve()


def _plain(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower().strip()


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", _plain(text)).strip("-") or "expediente"


def _visible_dirs(folder):
    return sorted((p for p in folder.iterdir() if p.is_dir() and not p.name.startswith(".")),
                  key=lambda p: p.name.lower())


def _human_size(size):
    for unit in ("B", "KB", "MB"):
        if size < 1024 or unit == "MB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return ""


def _is_document(path):
    return path.is_file() and not path.name.startswith((".", "~$")) and path.suffix.lower() in ALLOWED_EXTENSIONS


def _title(stem):
    title = stem.split(" - ")[0] if " - " in stem else stem
    return title.replace("_", " ").strip()


def _variant(path, root):
    ext = path.suffix.lower()
    return {
        "kind": ALLOWED_EXTENSIONS[ext],
        "ext": ext.lstrip("."),
        "size": _human_size(path.stat().st_size),
        "path": path.relative_to(root).as_posix(),
        "inline": ext in INLINE_EXTENSIONS,
    }


def _documents(paths, root):
    """Agrupa archivos con el mismo nombre (PDF + Word/Excel) en un solo documento."""
    by_stem = {}
    for p in paths:
        if _is_document(p):
            by_stem.setdefault((p.parent, p.stem.lower()), []).append(p)
    docs = []
    for files in by_stem.values():
        files.sort(key=lambda p: PREFERRED_ORDER.index(p.suffix.lower()))
        main, *others = files
        doc = {"name": _title(main.stem), **_variant(main, root)}
        doc["original"] = _variant(others[0], root) if others else None
        docs.append(doc)
    return sorted(docs, key=lambda d: _plain(d["name"]))


def _category(folder_name, files):
    label = re.sub(r"^\s*\d+[\s._-]*", "", folder_name).strip() or folder_name
    icon, hint = _CATEGORY_INFO.get(_plain(label), ("📁", ""))
    return {"name": label, "key": _plain(label), "icon": icon, "hint": hint, "files": files}


def _initials(name):
    parts = [p for p in re.split(r"\s+", name) if p]
    return "".join(p[0] for p in parts[:2]).upper()


def list_expedientes():
    """Un expediente por carpeta de ``expedientes/``, con sus documentos por categoría."""
    root = documents_root()
    base = root / "expedientes"
    if not base.is_dir():
        return []
    expedientes, used_slugs = [], set()
    for folder in _visible_dirs(base):
        if folder.name.lower() == MANUAL_FOLDER:
            continue
        categories = []
        loose = _documents(folder.iterdir(), root)
        for sub in _visible_dirs(folder):
            files = _documents(sub.rglob("*"), root)
            if files:
                categories.append(_category(sub.name, files))
        if loose:
            categories.append(_category(LOOSE_CATEGORY, loose))
        slug = _slug(folder.name)
        while slug in used_slugs:
            slug += "-2"
        used_slugs.add(slug)
        expedientes.append({
            "name": folder.name,
            "slug": slug,
            "initials": _initials(folder.name),
            "categories": categories,
            "total": sum(len(c["files"]) for c in categories),
        })
    return expedientes


def expedientes_summary(expedientes):
    return {
        "count": len(expedientes),
        "documents": sum(e["total"] for e in expedientes),
    }


def _manual_folder(root):
    """``manual/`` en la raíz o dentro de ``expedientes/`` (sin importar mayúsculas)."""
    for parent in (root, root / "expedientes"):
        if parent.is_dir():
            for p in _visible_dirs(parent):
                if p.name.lower() == MANUAL_FOLDER:
                    return p
    return None


def manual_documents():
    root = documents_root()
    base = _manual_folder(root)
    return _documents(base.rglob("*"), root) if base else []


def resolve_document(relative_path):
    """Ruta absoluta de un documento permitido, o None si no existe o sale de la carpeta."""
    root = documents_root()
    try:
        target = (root / relative_path).resolve()
        rel = target.relative_to(root)
    except (ValueError, OSError):
        return None
    if any(part.startswith(".") for part in rel.parts):
        return None
    return target if _is_document(target) else None


_CATEGORY_INFO.update({_plain(k): v for k, v in CATEGORY_INFO.items()})
