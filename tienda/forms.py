from django import forms
from .models import Perfil
from .models import Producto
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto  # Este es el modelo que utilizará el formulario
        fields = ['nombre', 'descripcion', 'precio', 'imagen']  # Aquí incluyes los campos del formulario

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen', 'direccion']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not "@" in email:
            raise ValidationError("El correo electrónico debe contener '@'.")
        return email