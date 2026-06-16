
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm

class FormularioNuevaContrasena(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'campo-input',
            'placeholder': 'Nueva contraseña',
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'campo-input',
            'placeholder': 'Confirmar nueva contraseña',
        })
        for field in self.fields.values():
            field.help_text = None

class FormularioRegistro(UserCreationForm):
    """Formulario de registro con email obligatorio."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'tu@email.com',
            'class': 'campo-input'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Nombre de usuario',
                'class': 'campo-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar los campos de contraseña
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'campo-input'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Confirmar contraseña',
            'class': 'campo-input'
        })
        # Quitar los textos de ayuda que Django pone por defecto
        for field in self.fields.values():
            field.help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class FormularioLogin(AuthenticationForm):
    """Formulario de login con estilos personalizados."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'placeholder': 'Nombre de usuario',
            'class': 'campo-input'
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'campo-input'
        })
        for field in self.fields.values():
            field.help_text = None