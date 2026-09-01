from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "interest", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Tu nombre",
                "autocomplete": "name",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "tu@email.com",
                "autocomplete": "email",
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "Teléfono (opcional)",
                "autocomplete": "tel",
            }),
            "interest": forms.Select(choices=[
                ("", "Selecciona una clase"),
                ("urbano", "Urbano"),
                ("contemporaneo", "Contemporáneo"),
                ("kpop", "K-pop"),
                ("otro", "Otra / información general"),
            ]),
            "message": forms.Textarea(attrs={
                "placeholder": "Cuéntanos qué te gustaría saber...",
                "rows": 4,
            }),
        }
