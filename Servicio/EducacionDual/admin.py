from django.contrib import admin
from .models import Empresas, Documento, Convocatoria, Postulacion, IngenieriaGaleria, Proyecto, Evidencia

admin.site.register(Documento)
admin.site.register(Empresas)
admin.site.register(Convocatoria)
admin.site.register(Postulacion)
admin.site.register(IngenieriaGaleria)
admin.site.register(Proyecto)
admin.site.register(Evidencia)

# Register your models here.
