from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Empresas, Documento, Convocatoria, Proyecto, Evidencia, IngenieriaGaleria, Index


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Correo electrónico'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Contraseña'}))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Número de Control',
            'email': 'Correo Electrónico',
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
        fields = ['Nombre', 'Apellidos', 'Carrera', 'Fecha_nacimiento', 'Genero', 'Telefono', 'Semestre']
        widgets = {
            'Fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'Nombre': 'Nombre',
            'Apellidos': 'Apellidos',
            
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

class ConvocatoriaForm(forms.ModelForm):
    class Meta:
        model = Convocatoria
        fields = [
            'titulo',
            'descripcion',
            'ingenierias',
            'empresa',
            'fecha_apertura',
            'fecha_cierre',
            'estado',
            'puesto'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'id': 'id_descripcion',
                'rows': 10,
                'placeholder': 'Escribe la descripción usando Markdown...'
            }),
            'fecha_apertura': forms.DateInput(attrs={'type': 'date'}),
            'fecha_cierre': forms.DateInput(attrs={'type': 'date'}),
            'ingenierias': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Quitar el required del HTML (para que no falle con EasyMDE)
        self.fields['descripcion'].required = False

    def clean(self):
        cleaned_data = super().clean()
        descripcion = cleaned_data.get('descripcion')

        # Validar en el servidor que no esté vacío
        if not descripcion or descripcion.strip() == "":
            self.add_error('descripcion', 'La descripción no puede estar vacía.')

        return cleaned_data
    
class IngenieriaGaleriaForm(forms.ModelForm):
    class Meta:
        model = IngenieriaGaleria
        fields = ['nombre', 'descripcion', 'imagen_portada', 'imagen_logo']

        labels = {
            'nombre': 'Nombre de la Ingeniería',
            'descripcion': 'Descripción',
            'imagen_portada': 'Imagen de Portada',
            'imagen_logo': 'Imagen de Logotipo',
        }

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['empresa', 'ingenieria', 'nombre', 'descripcion']

class EvidenciaForm(forms.ModelForm):
    class Meta:
        model = Evidencia
        fields = ['proyecto', 'titulo', 'descripcion', 'imagen']


class IndexForm(forms.ModelForm):
    class Meta:
        model = Index
        fields = ['Titulo', 'Texto', 'Imagen']