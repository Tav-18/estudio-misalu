from django.db import models

class ContactMessage(models.Model):
    name = models.CharField("Nombre", max_length=120)
    email = models.EmailField("Correo")
    phone = models.CharField("Teléfono", max_length=30, blank=True)
    interest = models.CharField("Clase de interés", max_length=40, blank=True)
    message = models.TextField("Mensaje")
    created_at = models.DateTimeField("Fecha", auto_now_add=True)
    is_read = models.BooleanField("Revisado", default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Mensaje de contacto"
        verbose_name_plural = "Mensajes de contacto"

    def __str__(self):
        return f"{self.name} - {self.email}"


def _choices(key):
    from .data import WORKER_FILTERS
    options = next(f["options"] for f in WORKER_FILTERS if f["key"] == key)
    return [(o, o) for o in options]


class Worker(models.Model):
    """Trabajador de Misalú (datos ficticios). Se muestra y se edita en el Área interna."""

    nombre = models.CharField("Nombre", max_length=120)
    cargo = models.CharField("Cargo", max_length=120)
    puesto = models.CharField("Puesto", max_length=40, choices=_choices("puesto"))
    area = models.CharField("Área", max_length=40, choices=_choices("area"))
    disciplina = models.CharField("Disciplina", max_length=40, blank=True, choices=_choices("disciplina"))
    tipo = models.CharField("Tipo de trabajador", max_length=40, choices=_choices("tipo"))
    estatus = models.CharField("Estatus", max_length=20, choices=_choices("estatus"), default="Activo")
    ingreso = models.PositiveSmallIntegerField("Año de ingreso", default=2024)

    class Meta:
        ordering = ["id"]
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"
