from django.db import migrations, models

# Personal inicial (el mismo del Directorio). Datos ficticios.
FIELDS = ("nombre", "cargo", "puesto", "area", "disciplina", "tipo", "estatus", "ingreso")
INITIAL_WORKERS = [
    ('Sara Romero', 'Directora general', 'Dirección', 'Dirección general', '', 'Tiempo completo', 'Activo', 2023),
    ('Nancy Rodríguez', 'Fundadora', 'Dirección', 'Dirección general', '', 'Tiempo completo', 'Activo', 2023),
    ('Alondra Laguna', 'Fundadora', 'Dirección', 'Dirección general', '', 'Tiempo completo', 'Activo', 2023),
    ('Iván Bello', 'Fundador', 'Dirección', 'Dirección general', '', 'Tiempo completo', 'Activo', 2023),
    ('Valeria Martínez', 'Directora académica', 'Dirección', 'Académica', '', 'Tiempo completo', 'Activo', 2023),
    ('Alejandro García', 'Maestro de urbano', 'Docente', 'Académica', 'Urbano', 'Medio tiempo', 'Activo', 2024),
    ('Daniela Sánchez', 'Maestra de urbano', 'Docente', 'Académica', 'Urbano', 'Tiempo completo', 'Activo', 2023),
    ('José Luis Morales', 'Maestro de K-pop', 'Docente', 'Académica', 'K-pop', 'Medio tiempo', 'Activo', 2024),
    ('Camila Vargas', 'Maestra de K-pop', 'Docente', 'Académica', 'K-pop', 'Medio tiempo', 'Activo', 2025),
    ('Roberto Flores', 'Maestro de contemporáneo', 'Docente', 'Académica', 'Contemporáneo', 'Tiempo completo', 'Activo', 2023),
    ('Andrea Castillo', 'Maestra de contemporáneo', 'Docente', 'Académica', 'Contemporáneo', 'Medio tiempo', 'Activo', 2024),
    ('Fernanda Ruiz', 'Maestra de K-pop', 'Docente', 'Académica', 'K-pop', 'Medio tiempo', 'Inactivo', 2023),
    ('Miguel Ángel Cruz', 'Director administrativo', 'Dirección', 'Administración', '', 'Tiempo completo', 'Activo', 2023),
    ('Sofía Mendoza', 'Tesorera', 'Administración', 'Administración', '', 'Tiempo completo', 'Activo', 2023),
    ('Luis Fernando Ortiz', 'Contabilidad', 'Administración', 'Administración', '', 'Medio tiempo', 'Activo', 2024),
    ('Paola Jiménez', 'Directora de marketing', 'Dirección', 'Marketing', '', 'Tiempo completo', 'Activo', 2023),
    ('Ricardo Navarro', 'Community manager', 'Marketing', 'Marketing', '', 'Medio tiempo', 'Activo', 2024),
    ('Karen Flores', 'Diseño y publicidad', 'Marketing', 'Marketing', '', 'Medio tiempo', 'Activo', 2024),
    ('Emmanuel Reyes', 'Eventos y presentaciones', 'Marketing', 'Marketing', '', 'Medio tiempo', 'Activo', 2025),
    ('Diego Hernández', 'Recursos Humanos', 'Recursos Humanos', 'Recursos Humanos', '', 'Tiempo completo', 'Activo', 2023),
    ('Natalia Cruz', 'Directora de servicios', 'Dirección', 'Servicios', '', 'Tiempo completo', 'Activo', 2023),
    ('Gabriela Torres', 'Recepción', 'Recepción', 'Servicios', '', 'Tiempo completo', 'Activo', 2024),
    ('Héctor Aguilar', 'Recepción (turno tarde)', 'Recepción', 'Servicios', '', 'Medio tiempo', 'Inactivo', 2024),
    ('Jorge Ramírez', 'Limpieza', 'Servicios', 'Servicios', '', 'Medio tiempo', 'Activo', 2024),
    ('Daniela Vargas', 'Mantenimiento', 'Servicios', 'Servicios', '', 'Medio tiempo', 'Activo', 2025),
]


def seed_workers(apps, schema_editor):
    Worker = apps.get_model("core", "Worker")
    Worker.objects.bulk_create([Worker(**dict(zip(FIELDS, row))) for row in INITIAL_WORKERS])


def unseed_workers(apps, schema_editor):
    apps.get_model("core", "Worker").objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Worker",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=120, verbose_name="Nombre")),
                ("cargo", models.CharField(max_length=120, verbose_name="Cargo")),
                (
                    "puesto",
                    models.CharField(
                        choices=[
                            ("Dirección", "Dirección"),
                            ("Docente", "Docente"),
                            ("Administración", "Administración"),
                            ("Marketing", "Marketing"),
                            ("Recursos Humanos", "Recursos Humanos"),
                            ("Recepción", "Recepción"),
                            ("Servicios", "Servicios"),
                        ],
                        max_length=40,
                        verbose_name="Puesto",
                    ),
                ),
                (
                    "area",
                    models.CharField(
                        choices=[
                            ("Dirección general", "Dirección general"),
                            ("Académica", "Académica"),
                            ("Administración", "Administración"),
                            ("Marketing", "Marketing"),
                            ("Recursos Humanos", "Recursos Humanos"),
                            ("Servicios", "Servicios"),
                        ],
                        max_length=40,
                        verbose_name="Área",
                    ),
                ),
                (
                    "disciplina",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Urbano", "Urbano"),
                            ("K-pop", "K-pop"),
                            ("Contemporáneo", "Contemporáneo"),
                        ],
                        max_length=40,
                        verbose_name="Disciplina",
                    ),
                ),
                (
                    "tipo",
                    models.CharField(
                        choices=[
                            ("Tiempo completo", "Tiempo completo"),
                            ("Medio tiempo", "Medio tiempo"),
                        ],
                        max_length=40,
                        verbose_name="Tipo de trabajador",
                    ),
                ),
                (
                    "estatus",
                    models.CharField(
                        choices=[("Activo", "Activo"), ("Inactivo", "Inactivo")],
                        default="Activo",
                        max_length=20,
                        verbose_name="Estatus",
                    ),
                ),
                (
                    "ingreso",
                    models.PositiveSmallIntegerField(
                        default=2024, verbose_name="Año de ingreso"
                    ),
                ),
            ],
            options={
                "verbose_name": "Trabajador",
                "verbose_name_plural": "Trabajadores",
                "ordering": ["id"],
            },
        ),
        migrations.RunPython(seed_workers, unseed_workers),
    ]
