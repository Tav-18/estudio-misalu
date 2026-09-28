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


from .models import Worker


class InternalLoginForm(forms.Form):
    email = forms.EmailField(label="Correo", widget=forms.EmailInput(attrs={
        "placeholder": "tu.correo@misalu.demo", "autocomplete": "username", "autofocus": True}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={
        "placeholder": "••••••••", "autocomplete": "current-password"}))


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ["nombre", "cargo", "puesto", "area", "disciplina", "tipo", "estatus", "ingreso"]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Nombre completo"}),
            "cargo": forms.TextInput(attrs={"placeholder": "Ej. Maestra de K-pop"}),
            "ingreso": forms.NumberInput(attrs={"min": 2000, "max": 2100}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["disciplina"].choices = [("", "— Sin disciplina —")] + list(self.fields["disciplina"].choices)[1:]
