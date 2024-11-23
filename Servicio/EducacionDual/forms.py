from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Empresas, Documento


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Correo electrónico'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Contraseña'}))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {
            'username': 'Número de Control',
            'password1': 'Contraseña',
            'password2': 'Confirmación de Contraseña',
        }
    
class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['Nombre', 'Apellidos', 'Correo_inst', 'Carrera', 'Fecha_nacimiento', 'Genero', 'Telefono', 'Semestre']
        widgets = {
            'Fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'Nombre': 'Nombre',
            'Apellidos': 'Apellidos',
            'Correo_inst': 'Correo Institucional',
            'Carrera': 'Carrera',
            'Fecha_nacimiento': 'Fecha de Nacimiento',
            'Genero': 'Género',
            'Telefono': 'Teléfono',
            'Semestre': 'Semestre',
        }

class EmpresasForm(forms.ModelForm):
    class Meta:
        model = Empresas
        fields = ['Nombre', 'Descripcion', 'Logotipo', 'Portada']
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la empresa'}),
            'Descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la empresa'}),
            'Portada': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'Logotipo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['titulo', 'archivo']