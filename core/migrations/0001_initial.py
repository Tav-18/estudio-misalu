from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Nombre")),
                ("email", models.EmailField(max_length=254, verbose_name="Correo")),
                ("phone", models.CharField(blank=True, max_length=30, verbose_name="Teléfono")),
                ("interest", models.CharField(blank=True, max_length=40, verbose_name="Clase de interés")),
                ("message", models.TextField(verbose_name="Mensaje")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha")),
                ("is_read", models.BooleanField(default=False, verbose_name="Revisado")),
            ],
            options={
                "verbose_name": "Mensaje de contacto",
                "verbose_name_plural": "Mensajes de contacto",
                "ordering": ["-created_at"],
            },
        ),
    ]
