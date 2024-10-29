from django.urls import path
from .views import (index, login_view, QueEs, Convocatorias, Normatividad,
                    Galeria, Empresas, baseAdmin, CustomLoginView, principalAdmin,logout_view)

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),  # URL para login de alumnos
    path('login_admin/', CustomLoginView.as_view(), name='login_admin'),
    path('QueEs/', QueEs, name='QueEs'),
    path('Convocatorias/', Convocatorias, name='Convocatorias'),
    path('Normatividad/', Normatividad, name='Normatividad'),
    path('Galeria/', Galeria, name='Galeria'),
    path('Empresas/', Empresas, name='Empresas'),
    path('baseAdmin/', baseAdmin, name='baseAdmin'),  # Dashboard de admin
    path('login_admin/', CustomLoginView.as_view(), name='login_admin'),
    path('principalAdmin/', principalAdmin, name='principalAdmin'),
    path('logout/', logout_view, name='logout'),
]
