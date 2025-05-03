from django.contrib import admin
from .models import Empresas, Documento, Convocatoria, Postulacion

admin.site.register(Documento)
admin.site.register(Empresas)
admin.site.register(Convocatoria)
admin.site.register(Postulacion)

# Register your models here.
