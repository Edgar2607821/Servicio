from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from .forms import LoginForm
# Colores Para el Diseño 
# Azul 1b396a, rgb(27, 57, 106), hsl(217, 59%, 26%)
# Blanco ffffff, rgb(255, 255, 255)

def index(request): 
    return render(request, 'EducacionDual/index.html')

def QueEs(request): 
    return render(request, 'EducacionDual/queEs.html')

def Normatividad(request): 
    return render(request, 'EducacionDual/Normatividad.html')

def Convocatorias(request): 
    return render(request, 'EducacionDual/Convocatorias.html')

def Empresas(request): 
    return render(request, 'EducacionDual/Empresas.html')

def Galeria(request): 
    return render(request, 'EducacionDual/Galeria.html')

def login_view(request):  # Vista de login para alumnos
    return render(request, 'EducacionDual/login.html')



@user_passes_test(lambda u: u.is_superuser)
def baseAdmin(request):  # Vista de dashboard del administrador
    return render(request, 'EducacionDual/baseAdministrador.html')

class CustomLoginView(LoginView):
    template_name = 'EducacionDual/loginAdmin.html'  # Reemplaza 'tu_template_de_login.html' con el nombre de tu plantilla
    form_class = LoginForm

@user_passes_test(lambda u: u.is_superuser)
def principalAdmin(request):
    nombre_usuario = request.user.username
    return render(request, 'EducacionDual/principalAdmin.html', {'nombre_usuario': nombre_usuario})

def logout_view(request):
    logout(request)  # Cierra la sesión
    return redirect('index')  # Redirige a la página de inicio después de cerrar sesión