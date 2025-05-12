from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import (EvidenciaForm, LoginForm, AuthenticationForm, CustomUserCreationForm, 
                    AdminProfileForm, ProyectoForm, UserProfileForm, EmpresasForm, DocumentoForm, 
                    ConvocatoriaForm, IngenieriaGaleriaForm, IndexForm)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash  # Evita que el usuario sea desconectado al cambiar la contraseña
from django.http import FileResponse, Http404, HttpResponse
from .models import Documento, UserProfile, Empresas, Convocatoria, Postulacion, IngenieriaGaleria, Proyecto, Evidencia, Index
from pdf2image import convert_from_path
from django.conf import settings
import os
from openpyxl import Workbook
from django.db.models import Count
from django.contrib.auth.decorators import login_required, user_passes_test
from collections import defaultdict
from django.db.models import Q



# Colores Para el Diseño 
# Azul 1b396a, rgb(27, 57, 106), hsl(217, 59%, 26%)
# Blanco ffffff, rgb(255, 255, 255)

def index(request): 
    
    return render(request, 'EducacionDual/index.html')

def QueEs(request): 
    Indexs = Index.objects.all()
    return render(request, 'EducacionDual/queEs.html', {'Indexs': Indexs})

def Normatividad(request):
    portadas = []

    # Asegúrate de que la carpeta media/portadas existe
    portada_folder = os.path.join(settings.MEDIA_ROOT, 'portadas')
    os.makedirs(portada_folder, exist_ok=True)

    # Itera sobre los documentos en la base de datos
    for documento in Documento.objects.all():
        pdf_path = documento.archivo.path  # Ruta completa del archivo PDF
        print(f"Intentando convertir el archivo PDF en: {pdf_path}")

        try:
            # Verifica que el archivo PDF exista
            if not os.path.exists(pdf_path):
                print(f"Archivo no encontrado: {pdf_path}")
                continue

            # Convierte la primera página del PDF a una imagen
            portada = convert_from_path(pdf_path, first_page=1, last_page=1, poppler_path=r'C:\poppler-24.08.0\Library\bin')[0]
            
            # Guarda la portada en la carpeta media/portadas
            portada_path = os.path.join(portada_folder, f'portada_{documento.id}.jpg')
            portada.save(portada_path, 'JPEG')
            print(f"Portada guardada en: {portada_path}")

            # Agrega el título del documento y la URL de la portada a la lista
            portadas.append({
                'documento_id': documento.id,  # Incluye el ID del documento
                'titulo': documento.titulo, 
                'portada_url': settings.MEDIA_URL + f'portadas/portada_{documento.id}.jpg'
            })
        
        except Exception as e:
            print(f"Error al generar portada para {documento.titulo}: {e}")

    return render(request, 'EducacionDual/Normatividad.html', {'portadas': portadas})

def Convocatorias(request): 
    convocatorias = Convocatoria.objects.filter(estado='Habilitada')  # O el estado que uses para "disponible"
    return render(request, 'EducacionDual/Convocatorias.html', {'convocatorias': convocatorias})

def detalle_convocatoria(request, convocatoria_id):
    convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)
    return render(request, 'EducacionDual/detalle_convocatoria.html', {'convocatoria': convocatoria})

def Empresas_Prin(request): 
    empresas = Empresas.objects.all()
    return render(request, 'EducacionDual/Empresas.html', {'empresas': empresas})

def Empresa_Detalle(request, empresa_id):
    empresa = get_object_or_404(Empresas, id=empresa_id)
    return render(request, 'EducacionDual/EmpresasDetalle.html', {'empresa': empresa})


def Galeria(request): 
    empresas = Empresas.objects.annotate(
        num_proyectos=Count('proyecto')
    )
    return render(request, 'EducacionDual/Galeria.html', {'empresas': empresas})

def Galeria_ingenierias(request, empresa_id):
    empresa = get_object_or_404(Empresas, id=empresa_id)
    proyectos = Proyecto.objects.filter(empresa=empresa)
    ingenierias = IngenieriaGaleria.objects.filter(id__in=proyectos.values_list('ingenieria_id', flat=True).distinct())
    return render(request, 'EducacionDual/galeria_ingenierias.html', {'empresa': empresa, 'ingenierias': ingenierias})



def Galeria_proyectos(request, empresa_id, ingenieria_id):
    empresa = get_object_or_404(Empresas, id=empresa_id)
    ingenieria = get_object_or_404(IngenieriaGaleria, id=ingenieria_id)
    proyectos = Proyecto.objects.filter(empresa=empresa, ingenieria=ingenieria)
    return render(request, 'EducacionDual/galeria_proyectos.html', {
        'empresa': empresa,
        'ingenieria': ingenieria,
        'proyectos': proyectos
    })

def Galeria_evidencias(request, empresa_id, ingenieria_id, proyecto_id):
    empresa = get_object_or_404(Empresas, id=empresa_id)
    ingenieria = get_object_or_404(IngenieriaGaleria, id=ingenieria_id)
    proyecto = get_object_or_404(Proyecto, id=proyecto_id, empresa=empresa, ingenieria=ingenieria)
    evidencias = Evidencia.objects.filter(proyecto=proyecto)
    return render(request, 'EducacionDual/galeria_evidencias.html', {
        'empresa': empresa, 
        'ingenieria': ingenieria,
        'proyecto': proyecto,
        'evidencias': evidencias
    })

@login_required
def principalAlumno(request):
    return render(request, 'EducacionDual/principalAlumno.html')

def terminosDeUso(request):
    return render(request, 'EducacionDual/terminosDeUso.html')

def politicaDePrivacidad(request):
    return render(request, 'EducacionDual/politicaDePrivacidad.html')


def register_user_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Inicia sesión automáticamente al usuario registrado
            login(request, user)
            return redirect('complete_profile')  # Redirige a la página de inicio o a la que elijas
    else:
        form = CustomUserCreationForm()
    return render(request, 'EducacionDual/Registrate.html', {'form': form})

#Login De Alumno

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_superuser:  # Verifica que el usuario no sea un admin
                login(request, user)
                return redirect('principalAlumno')  # Redirige al área de usuarios normales
            else:
                return render(request, 'EducacionDual/login.html', {'form': form, 'error': 'No tiene permisos para iniciar sesión aquí'})
    else:
        form = AuthenticationForm()
    return render(request, 'EducacionDual/login.html', {'form': form})

@login_required
def Alumno_perfil_view(request):
    # Verifica que el usuario no sea un superusuario
    if request.user.is_superuser:
        return redirect('admin_profile')  # Redirige a la página de perfil de admin si es superusuario

    # Obtiene el perfil del usuario actual
    profile = UserProfile.objects.get(NoControl=request.user)

    return render(request, 'EducacionDual/perfilAlumno.html', {'profile': profile})

@login_required
def edit_Alumno_profile_view(request):
    # Obtiene el perfil del usuario, o lo crea si no existe
    profile, created = UserProfile.objects.get_or_create(NoControl=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('Alumno_perfil')  # Redirige a la página de detalles del perfil después de guardar
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'EducacionDual/editar_Perfil_Alum.html', {'form': form})


def complete_profile(request):
    # Obtiene el perfil del usuario, o lo crea si no existe
    profile, created = UserProfile.objects.get_or_create(NoControl=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('Alumno_perfil')  # Redirige a la página de detalles del perfil después de guardar
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'EducacionDual/complete_profile.html', {'form': form})

@login_required
def principalAlumno(request):
    perfil = request.user.userprofile
    nombre_completo = f"{perfil.Nombre}"
    return render(request, 'EducacionDual/principalAlumno.html', {'nombre_completo': nombre_completo})

@login_required
def convocatorias_alumno(request):
    alumno = request.user.userprofile
    carrera = alumno.Carrera  # Debe coincidir con las opciones del campo ingenierias de la convocatoria

    convocatorias = Convocatoria.objects.filter(
        estado="Habilitada",
        ingenierias__contains=carrera
    )
    return render(request, 'EducacionDual/convocatorias_list_alumno.html', {'convocatorias': convocatorias})

@login_required
def convocatoria_detalle_alumno(request, convocatoria_id):
    convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)
    alumno = request.user.userprofile

    ya_postulado = Postulacion.objects.filter(convocatoria=convocatoria, alumno=alumno).exists()
    
    

    return render(request, 'EducacionDual/convocatoria_detail_alumno.html', {
        'convocatoria': convocatoria,
        'ya_postulado': ya_postulado
    })


@login_required
def postularse(request, convocatoria_id):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para postularte.")
        return redirect('login')

    alumno = get_object_or_404(UserProfile, NoControl=request.user)
    convocatoria = get_object_or_404(Convocatoria, pk=convocatoria_id)

    if Postulacion.objects.filter(alumno=alumno, convocatoria=convocatoria).exists():
        messages.warning(request, "Ya te has postulado a esta convocatoria.")
    else:
        Postulacion.objects.create(alumno=alumno, convocatoria=convocatoria)
        messages.success(request, "Te has postulado exitosamente.")

    return redirect('convocatoria_detalle_alumno', convocatoria_id=convocatoria_id)

@login_required
def todas_las_postulaciones(request):
    postulaciones = Postulacion.objects.select_related('alumno', 'convocatoria').all()
    return render(request, 'EducacionDual/postulacion_list_todas.html', {'postulaciones': postulaciones})


@login_required
def postulacion_detalle(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        nuevas_observaciones = request.POST.get('observaciones', '')
        if nuevo_estado in ['Pendiente', 'Aceptado', 'Rechazado']:
            postulacion.estado = nuevo_estado
            postulacion.observaciones = nuevas_observaciones
            postulacion.save()
            messages.success(request, 'Estado actualizado correctamente.')
            return redirect('todas_las_postulaciones')

    return render(request, 'EducacionDual/postulacion_detail.html', {
        'postulacion': postulacion
    })

@login_required
def mis_postulaciones(request):
    alumno = request.user.userprofile
    postulaciones = Postulacion.objects.filter(alumno=alumno).select_related('convocatoria').order_by('-fecha_postulacion')
    return render(request, 'EducacionDual/mis_postulaciones.html', {'postulaciones': postulaciones})

#Administrador/Profesor
@user_passes_test(lambda u: u.is_superuser)
def baseAdmin(request):  # Vista de dashboard del administrador
    return render(request, 'EducacionDual/baseAdministrador.html')


#Login de Admin

class AdminRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login_admin')


def login_admin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:  # Verifica que el usuario sea un admin
                login(request, user)
                return redirect('principalAdmin')  # Redirige al área de admin
            else:
                return render(request, 'EducacionDual/loginAdmin.html', {'form': form, 'error': 'Acceso denegado'})
    else:
        form = AuthenticationForm()
    return render(request, 'EducacionDual/loginAdmin.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('QueEs')  # Redirige a la página de inicio de sesión después de cerrar sesión


@user_passes_test(lambda u: u.is_superuser)
def principalAdmin(request):
    nombre_usuario = request.user.username
    return render(request, 'EducacionDual/principalAdmin.html', {'nombre_usuario': nombre_usuario})


@login_required
def admin_profile_view(request):
    # Verifica si el usuario tiene permisos de administrador
    if request.user.is_superuser:
        return render(request, 'EducacionDual/perfilAdmin.html', {'admin_user': request.user})
    else:
        # Redirige o muestra un mensaje de error si no es administrador
        return redirect('QueEs')  # Redirige a la página de inicio u otra página

@login_required
def edit_admin_profile_view(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirige si el usuario no es administrador

    if request.method == 'POST':
        profile_form = AdminProfileForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if profile_form.is_valid() and password_form.is_valid():
            # Guarda los cambios en el perfil
            profile_form.save()
            # Guarda el cambio de contraseña
            password_form.save()
            # Mantiene la sesión activa tras el cambio de contraseña
            update_session_auth_hash(request, password_form.user)
            return redirect('admin_profile')  # Redirige al perfil después de guardar
        else:
            print(profile_form.errors)  # Depuración: muestra errores del formulario de perfil
            print(password_form.errors)  # Depuración: muestra errores del formulario de contraseña
    else:
        profile_form = AdminProfileForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'EducacionDual/edit_admin_perfil.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })
@login_required
def lista_Alumnos_view(request):
    users = User.objects.filter(is_superuser=False)  # Obtiene todos los usuarios
    return render(request, 'EducacionDual/lista_Alumnos.html', {'users': users})

@login_required
def Alumno_perfil_detalle_view(request, user_id):
    profile = get_object_or_404(UserProfile, NoControl__id=user_id)
    return render(request, 'EducacionDual/Alumno_perfil_detalle.html', {'profile': profile})

@login_required
def eliminar_alumno(request, alumno_id):
    alumno = get_object_or_404(UserProfile, id=alumno_id)
    usuario = alumno.NoControl  # El User asociado
    if request.method == 'POST':
        alumno.delete()
        usuario.delete()   # Elimina el usuario (auth_user)
        messages.success(request, "El alumno ha sido eliminado correctamente.")
        return redirect('lista_Alumnos')  # Cambia al nombre correcto de tu lista de alumnos

    return render(request, 'EducacionDual/alumno_confirm_delete.html', {'alumno': alumno})

@login_required
def empresas_detalle_view(request):
    empresas = Empresas.objects.all()
    return render(request, 'EducacionDual/listaEmpresas.html', {'empresas': empresas})

@login_required
def crear_empresa(request):
    if request.method == 'POST':
        form = EmpresasForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_empresas')  # Redirige a una página de lista o detalle
    else:
        form = EmpresasForm()
    return render(request, 'EducacionDual/crear_empresa.html', {'form': form})

@login_required
def editar_empresa_view(request, empresa_id):
    empresa = get_object_or_404(Empresas, id=empresa_id)
    if request.method == 'POST':
        form = EmpresasForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect('lista_empresas')  # Redirige a la lista de empresas después de editar
    else:
        form = EmpresasForm(instance=empresa)
    return render(request, 'EducacionDual/editar_empresa.html', {'form': form, 'empresa': empresa})

@login_required
def eliminar_empresa_view(request, empresa_id):
    empresa = get_object_or_404(Empresas, id=empresa_id)
    if request.method == 'POST':
        empresa.delete()
        return redirect('lista_empresas')
    return render(request, 'EducacionDual/eliminar_empresa.html', {'empresa': empresa})


@login_required
def lista_documentos_view(request):
    documentos = Documento.objects.all()
    return render(request, 'EducacionDual/lista_documentos.html', {'documentos': documentos})


@login_required
def crear_documento_view(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_documentos')
    else:
        form = DocumentoForm()
    return render(request, 'EducacionDual/crear_documento.html', {'form': form})



# Vista para editar un documento
@login_required
def editar_documento_view(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            return redirect('lista_documentos')
    else:
        form = DocumentoForm(instance=documento)
    return render(request, 'EducacionDual/editar_documento.html', {'form': form, 'documento': documento})

# Vista para eliminar un documento
@login_required
def eliminar_documento_view(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    if request.method == 'POST':
        documento.delete()
        return redirect('lista_documentos')
    return render(request, 'EducacionDual/eliminar_documento.html', {'documento': documento})

@login_required
def mostrar_pdf(request, documento_id):
    try:
        documento = Documento.objects.get(pk=documento_id)
        # FileResponse puede abrir el archivo en el navegador si el navegador soporta el tipo de contenido
        response = FileResponse(documento.archivo.open('rb'), content_type='application/pdf')
        # Especifica que no deseas forzar la descarga removiendo el encabezado 'Content-Disposition'
        response['Content-Disposition'] = 'inline; filename="{}"'.format(documento.archivo.name)
        return response
    except Documento.DoesNotExist:
        raise Http404("Documento no encontrado")
    
# Lista de convocatorias

class ConvocatoriaListView(AdminRequiredMixin, ListView):
    model = Convocatoria
    template_name = 'EducacionDual/convocatoria_list.html'
    context_object_name = 'convocatorias'

# Detalle de una convocatoria

class ConvocatoriaDetailView(AdminRequiredMixin, DetailView):
    model = Convocatoria
    template_name = 'EducacionDual/convocatoria_detail.html'

# Crear convocatoria

class ConvocatoriaCreateView(AdminRequiredMixin, CreateView):
    model = Convocatoria
    form_class = ConvocatoriaForm
    template_name = 'EducacionDual/convocatoria_form.html'
    success_url = reverse_lazy('convocatoria_list')

# Actualizar convocatoria

class ConvocatoriaUpdateView(AdminRequiredMixin, UpdateView):
    model = Convocatoria
    form_class = ConvocatoriaForm
    template_name = 'EducacionDual/convocatoria_form.html'
    success_url = reverse_lazy('convocatoria_list')

# Eliminar convocatoria

class ConvocatoriaDeleteView(AdminRequiredMixin, DeleteView):
    model = Convocatoria
    template_name = 'EducacionDual/convocatoria_confirm_delete.html'
    success_url = reverse_lazy('convocatoria_list')
    
@login_required
def eliminar_postulacion(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)

    if request.method == 'POST':
        postulacion.delete()
        messages.success(request, 'La postulación ha sido eliminada correctamente.')
        return redirect('todas_las_postulaciones')

    return render(request, 'EducacionDual/eliminar_postulacion.html', {
        'postulacion': postulacion
    })

# Lista de ingenierías
@login_required
def lista_ingenierias(request):
    ingenierias = IngenieriaGaleria.objects.all()
    return render(request, 'EducacionDual/lista_ingenierias.html', {'ingenierias': ingenierias})

# Crear nueva ingeniería
@login_required
def crear_ingenieria(request):
    if request.method == 'POST':
        form = IngenieriaGaleriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingeniería creada exitosamente.')
            return redirect('lista_ingenierias')
    else:
        form = IngenieriaGaleriaForm()
    return render(request, 'EducacionDual/form_ingenieria.html', {'form': form, 'titulo': 'Crear Ingeniería'})

# Editar ingeniería
@login_required
def editar_ingenieria(request, pk):
    ingenieria = get_object_or_404(IngenieriaGaleria, pk=pk)
    if request.method == 'POST':
        form = IngenieriaGaleriaForm(request.POST, request.FILES, instance=ingenieria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingeniería actualizada exitosamente.')
            return redirect('lista_ingenierias')
    else:
        form = IngenieriaGaleriaForm(instance=ingenieria)
    return render(request, 'EducacionDual/form_ingenieria.html', {'form': form, 'titulo': 'Editar Ingeniería'})

# Eliminar ingeniería
@login_required
def eliminar_ingenieria(request, pk):
    ingenieria = get_object_or_404(IngenieriaGaleria, pk=pk)
    if request.method == 'POST':
        ingenieria.delete()
        messages.success(request, 'Ingeniería eliminada exitosamente.')
        return redirect('lista_ingenierias')
    return render(request, 'EducacionDual/confirmar_eliminar_ingenieria.html', {'ingenieria': ingenieria})



# Lista de proyectos
@login_required
def lista_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'EducacionDual/lista_proyectos.html', {'proyectos': proyectos})

# Crear nuevo proyecto
@login_required
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proyecto creado exitosamente.')
            return redirect('lista_proyectos')
    else:
        form = ProyectoForm()
    return render(request, 'EducacionDual/form_proyecto.html', {'form': form, 'titulo': 'Crear Proyecto'})

# Editar proyecto
@login_required
def editar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proyecto actualizado exitosamente.')
            return redirect('lista_proyectos')
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'EducacionDual/form_proyecto.html', {'form': form, 'titulo': 'Editar Proyecto'})

# Eliminar proyecto
@login_required
def eliminar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        proyecto.delete()
        messages.success(request, 'Proyecto eliminado exitosamente.')
        return redirect('lista_proyectos')
    return render(request, 'EducacionDual/confirmar_eliminar_proyecto.html', {'proyecto': proyecto})

# Lista de evidencias
@login_required
def lista_evidencias(request):
    evidencias = Evidencia.objects.all()
    return render(request, 'EducacionDual/lista_evidencias.html', {'evidencias': evidencias})

# Crear nueva evidencia
@login_required
def crear_evidencia(request):
    if request.method == 'POST':
        form = EvidenciaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evidencia agregada exitosamente.')
            return redirect('lista_evidencias')
    else:
        form = EvidenciaForm()
    return render(request, 'EducacionDual/form_evidencia.html', {'form': form, 'titulo': 'Agregar Evidencia'})

# Editar evidencia
@login_required
def editar_evidencia(request, pk):
    evidencia = get_object_or_404(Evidencia, pk=pk)
    if request.method == 'POST':
        form = EvidenciaForm(request.POST, request.FILES, instance=evidencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evidencia actualizada exitosamente.')
            return redirect('lista_evidencias')
    else:
        form = EvidenciaForm(instance=evidencia)
    return render(request, 'EducacionDual/form_evidencia.html', {'form': form, 'titulo': 'Editar Evidencia'})

# Eliminar evidencia
@login_required
def eliminar_evidencia(request, pk):
    evidencia = get_object_or_404(Evidencia, pk=pk)
    if request.method == 'POST':
        evidencia.delete()
        messages.success(request, 'Evidencia eliminada exitosamente.')
        return redirect('lista_evidencias')
    return render(request, 'EducacionDual/confirmar_eliminar_evidencia.html', {'evidencia': evidencia})

@login_required
def GaleriaAdmin(request): 
    return render(request, 'EducacionDual/GaleriaAdmin.html')

class IndexListView(AdminRequiredMixin, ListView):
    model = Index
    template_name = 'EducacionDual/Index_list.html'
    context_object_name = 'indexs'

# Detalle de Index



class IndexCreateView(AdminRequiredMixin, CreateView):
    model = Index
    form_class = IndexForm
    template_name = 'EducacionDual/Index_form.html'
    success_url = reverse_lazy('index_list')

# Actualizar Index

class IndexUpdateView(AdminRequiredMixin, UpdateView):
    model = Index
    form_class = IndexForm
    template_name = 'EducacionDual/Index_form.html'
    success_url = reverse_lazy('index_list')

# Eliminar Index

class IndexDeleteView(AdminRequiredMixin, DeleteView):
    model = Index
    template_name = 'EducacionDual/Index_confirm_delete.html'
    success_url = reverse_lazy('index_list')

def exportar_postulaciones_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Postulaciones"

    # Encabezados (agrega "No." al inicio)
    ws.append([
        "No.", "Alumno", "No. Control", "Correo", "Carrera", "Semestre", "Teléfono",
        "Convocatoria", "Puesto", "Empresa", "Fecha de Apertura", "Fecha de Cierre", "Fecha de Postulación", "Estado", "Observaciones"
    ])

    postulaciones = Postulacion.objects.select_related('alumno', 'convocatoria')

    for i, p in enumerate(postulaciones, start=1):
        alumno = f"{p.alumno.Nombre} {p.alumno.Apellidos}"
        nocontrol = p.alumno.NoControl.username
        correo = p.alumno.NoControl.email
        carrera = p.alumno.Carrera
        semestre = p.alumno.Semestre
        telefono = p.alumno.Telefono
        convocatoria = p.convocatoria.titulo
        puesto = p.convocatoria.puesto
        empresa = p.convocatoria.empresa.Nombre
        fecha_apertura = p.convocatoria.fecha_apertura.strftime('%d/%m/%Y') if p.convocatoria.fecha_apertura else ''
        fecha_cierre = p.convocatoria.fecha_cierre.strftime('%d/%m/%Y') if p.convocatoria.fecha_cierre else ''
        fecha_postulacion = p.fecha_postulacion.strftime('%d/%m/%Y %H:%M') if p.fecha_postulacion else ''
        estado = p.estado
        observaciones = p.observaciones

        ws.append([
            i, alumno, nocontrol, correo, carrera, semestre, telefono,
            convocatoria, puesto, empresa, fecha_apertura, fecha_cierre, fecha_postulacion, estado, observaciones
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=postulaciones_completas.xlsx'
    wb.save(response)
    return response


@login_required
def estadisticasg(request):
    # Usuarios
    total_usuarios = UserProfile.objects.filter(~Q(NoControl__isnull=True)).count()
    total_usuariosAlumn = total_usuarios - 1  # Descontar al admin (ajustar si es necesario)

    perfiles_completados = UserProfile.objects.filter(
        ~Q(Nombre__isnull=True), ~Q(Nombre=''),
        ~Q(Apellidos__isnull=True), ~Q(Apellidos=''),
        ~Q(Carrera__isnull=True), ~Q(Carrera=''),
        ~Q(Fecha_nacimiento__isnull=True),
        ~Q(Genero__isnull=True), ~Q(Genero=''),
        ~Q(Telefono__isnull=True), ~Q(Telefono=''),
        ~Q(Semestre__isnull=True), ~Q(Semestre='')
    ).count()

    # Convocatorias
    convocatorias_activas = Convocatoria.objects.filter(estado="Habilitada").count()
    convocatorias_inactivas = Convocatoria.objects.filter(estado="Deshabilitada").count()
    convocatorias_totales = convocatorias_activas + convocatorias_inactivas

    # Postulaciones
    total_postulaciones = Postulacion.objects.count()
    aceptadas = Postulacion.objects.filter(estado='Aceptado').count()
    rechazadas = Postulacion.objects.filter(estado='Rechazado').count()
    pendientes = Postulacion.objects.filter(estado='Pendiente').count()

    # Empresas
    total_empresas = Empresas.objects.count()

    # Proyectos y evidencias
    total_proyectos = Proyecto.objects.count()
    total_evidencias = Evidencia.objects.count()

    contexto = {
        'total_usuarios': total_usuariosAlumn,
        'perfiles_completados': perfiles_completados,
        'convocatorias_activas': convocatorias_activas,
        'convocatorias_inactivas': convocatorias_inactivas,
        'convocatorias_totales': convocatorias_totales,
        'total_postulaciones': total_postulaciones,
        'aceptadas': aceptadas,
        'rechazadas': rechazadas,
        'pendientes': pendientes,
        'total_empresas': total_empresas,
        'total_proyectos': total_proyectos,
        'total_evidencias': total_evidencias,
    }

    return render(request, 'EducacionDual/estadisticas_generales.html', contexto)



def graficas_totales_por_ingenieria(request):
    ABREVIATURAS = {
        "INGENIERÍA INDUSTRIAL": "II",
        "INGENIERÍA INDUSTRIAL MIXTA": "II-M",
        "INGENIERÍA EN GESTIÓN EMPRESARIAL": "IGE",
        "INGENIERÍA EN GESTIÓN EMPRESARIAL MIXTA": "IGE-M",
        "INGENIERÍA EN SISTEMAS COMPUTACIONALES": "ISC",
        "INGENIERÍA AMBIENTAL": "IAMB",
        "INGENIERÍA EN INDUSTRIAS ALIMENTARIAS": "IIAL",
        "INGENIERÍA EN AGRONOMÍA": "IAGR",
        "INGENIERÍA EN INTELIGENCIA ARTIFICIAL": "IIAR",
        "INGENIERÍA EN DESARROLLO DE APLICACIONES": "IDA",
    }

    usuarios = UserProfile.objects.filter(Carrera__isnull=False, Genero__isnull=False).exclude(Carrera='', Genero='')

    datos = defaultdict(lambda: {'Femenino': 0, 'Masculino': 0, 'Otro': 0})
    resumen = []

    for user in usuarios:
        carrera = user.Carrera
        genero = user.Genero
        datos[carrera][genero] += 1

    for carrera, generos in datos.items():
        nombre_completo = carrera
        abreviatura = ABREVIATURAS.get(carrera, carrera)
        total = sum(generos.values())

        resumen.append({
            'nombre_completo': nombre_completo,
            'abreviatura': abreviatura,
            'total': total,
            'generos': generos
        })

    return render(request, 'EducacionDual/graficas_totales_por_ingenieria.html', {
        'datos_por_carrera': resumen
    })


def graficas_por_carrera(request):
    ABREVIATURAS = {
        "INGENIERÍA INDUSTRIAL": "II",
        "INGENIERÍA INDUSTRIAL MIXTA": "II-M",
        "INGENIERÍA EN GESTIÓN EMPRESARIAL": "IGE",
        "INGENIERÍA EN GESTIÓN EMPRESARIAL MIXTA": "IGE-M",
        "INGENIERÍA EN SISTEMAS COMPUTACIONALES": "ISC",
        "INGENIERÍA AMBIENTAL": "IAMB",
        "INGENIERÍA EN INDUSTRIAS ALIMENTARIAS": "IIAL",
        "INGENIERÍA EN AGRONOMÍA": "IAGR",
        "INGENIERÍA EN INTELIGENCIA ARTIFICIAL": "IIAR",
        "INGENIERÍA EN DESARROLLO DE APLICACIONES": "IDA",
    }

    postulaciones = Postulacion.objects.filter(
        alumno__Carrera__isnull=False,
        alumno__Genero__isnull=False
    ).exclude(
        alumno__Carrera='',
        alumno__Genero=''
    )

    conteo_por_carrera = defaultdict(lambda: {'Femenino': 0, 'Masculino': 0, 'Otro': 0})
    for p in postulaciones:
        carrera = p.alumno.Carrera
        genero = p.alumno.Genero
        conteo_por_carrera[carrera][genero] += 1

    # Convertimos a lista de dicts con abreviatura y nombre completo
    datos_finales = []
    for carrera, generos in conteo_por_carrera.items():
        total = sum(generos.values())
        datos_finales.append({
            'nombre_completo': carrera,
            'abreviatura': ABREVIATURAS.get(carrera, carrera),
            'generos': generos,
            'total': total
        })

    return render(request, 'EducacionDual/graficas_por_carrera.html', {
        'datos_por_carrera': datos_finales
    })

def estadisticas(request): 
    return render(request, 'EducacionDual/estadisticas.html')

    
def estadisticas_status(request): 
    datos_empresas = (
        Postulacion.objects
        .values('convocatoria__empresa__Nombre')
        .annotate(
            aceptados=Count('id', filter=Q(estado='Aceptado')),
            rechazados=Count('id', filter=Q(estado='Rechazado')), 
            pendientes=Count('id', filter=Q(estado='Pendiente')), 
        )
    )

    datos_empresas = list(datos_empresas)
    mitad = len(datos_empresas) // 2
    datos_izquierda = datos_empresas[:mitad]
    datos_derecha = datos_empresas[mitad:]

    context = {
        'datos_izquierda': datos_izquierda,
        'datos_derecha': datos_derecha,
    }

    return render(request, 'EducacionDual/estadisticas_status.html', context)


def postulaciones_por_empresa(request):
    # Gráfica general: total de postulaciones por empresa
    postulaciones = (
        Postulacion.objects
        .values('convocatoria__empresa__Nombre')
        .annotate(total_postulaciones=Count('id'))
        .order_by('convocatoria__empresa__Nombre')
    )

    # Gráficas individuales: postulaciones por género y empresa
    datos_por_empresa = defaultdict(lambda: {'Femenino': 0, 'Masculino': 0, 'Otro': 0})

    for p in Postulacion.objects.select_related('alumno', 'convocatoria__empresa'):
        empresa = p.convocatoria.empresa.Nombre if p.convocatoria and p.convocatoria.empresa else None
        genero = p.alumno.Genero if p.alumno else None

        if empresa and genero:
            datos_por_empresa[empresa][genero] += 1

    return render(request, 'EducacionDual/postulaciones_por_empresa.html', {
        'postulaciones': postulaciones,
        'datos_por_empresa': dict(datos_por_empresa)
    })


def postulaciones_por_semestre(request):
    # Obtener el total de postulaciones por semestre
    postulaciones = Postulacion.objects.values('alumno__Semestre') \
        .annotate(total_postulaciones=Count('id')) \
        .order_by('alumno__Semestre')
    
    # Pasar los datos a la plantilla
    return render(request, 'EducacionDual/postulaciones_por_semestre.html', {
        'postulaciones': postulaciones
    })