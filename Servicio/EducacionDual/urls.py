from django.urls import path
from .views import (index, login_view, QueEs, Convocatorias, Normatividad,
                    Galeria, Empresas_Prin, baseAdmin, login_admin_view, principalAdmin,logout_view, mostrar_pdf,
                    register_user_view, principalAlumno,admin_profile_view, edit_admin_profile_view, lista_Alumnos_view,
                    Alumno_perfil_detalle_view, edit_Alumno_profile_view, Alumno_perfil_view, empresas_detalle_view, crear_empresa,
                    editar_empresa_view,lista_documentos_view, crear_documento_view, editar_documento_view, eliminar_documento_view,
                    complete_profile, eliminar_empresa_view)

urlpatterns = [
    path('', QueEs, name='QueEs'),
    path('login/', login_view, name='login'),  # URL para login de alumnos
    path('login_admin_view/', login_admin_view, name='login_admin'),
    path('Convocatorias/', Convocatorias, name='Convocatorias'),
    path('Normatividad/', Normatividad, name='Normatividad'),
    path('Galeria/', Galeria, name='Galeria'),
    path('Empresas/', Empresas_Prin, name='Empresas'),
    path('baseAdmin/', baseAdmin, name='baseAdmin'),  # Dashboard de admin
    path('principalAdmin/', principalAdmin, name='principalAdmin'),
    path('logout/', logout_view, name='logout'),
    path('ver-pdf/<int:documento_id>/', mostrar_pdf, name='mostrar_pdf'),
    path('Registrate', register_user_view, name='Registrate'),
    path('principalAlumno', principalAlumno, name='principalAlumno'),
    path('admin_profile/', admin_profile_view, name='admin_profile'),
    path('admin_profile/edit/', edit_admin_profile_view, name='edit_admin_profile'),
    path('lista_Alumnos/', lista_Alumnos_view, name='lista_Alumnos'),
    path('Alumno_perfil_detalle/<int:user_id>/', Alumno_perfil_detalle_view, name='Alumno_perfil_detalle'),
    path('edit_Alumno/', edit_Alumno_profile_view, name='edit_Alumno'),
    path('complete_profile/', complete_profile, name='complete_profile'),
    path('Alumno_perfil/', Alumno_perfil_view, name='Alumno_perfil'),
    path('lista_empresas/', empresas_detalle_view, name='lista_empresas'),
    path('crear_empresa/', crear_empresa, name='crear_empresa'),
    path('editar_empresa/<int:empresa_id>/', editar_empresa_view, name='editar_empresa'),
    path('eliminar_empresa/<int:empresa_id>/', eliminar_empresa_view, name='eliminar_empresa'),
    path('documentos/', lista_documentos_view, name='lista_documentos'),
    path('documentos/crear/', crear_documento_view, name='crear_documento'),
    path('documentos/<int:documento_id>/editar/', editar_documento_view, name='editar_documento'),
    path('documentos/<int:documento_id>/eliminar/', eliminar_documento_view, name='eliminar_documento'),
]
