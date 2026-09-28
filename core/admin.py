from django.contrib import admin
from .models import ContactMessage, Worker

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "interest", "created_at", "is_read")
    list_filter = ("interest", "is_read", "created_at")
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = ("created_at",)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cargo", "puesto", "area", "disciplina", "tipo", "estatus")
    list_filter = ("puesto", "area", "disciplina", "tipo", "estatus")
    search_fields = ("nombre", "cargo")
