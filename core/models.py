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
