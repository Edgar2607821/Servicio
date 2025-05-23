from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError



def validar_tamano_imagen(imagen):
    limite_mb = 2  # por ejemplo, 2MB
    if imagen.size > limite_mb * 1024 * 1024:
        raise ValidationError(f"La imagen no puede pesar más de {limite_mb} MB.")


# Create your models here. 

class UserProfile(models.Model):
    SEXO_CHOICES = [
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),
        ('Otro', 'Otro')
    ]

    SEMESTRES_CHOICES = [
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
    ]
    
    CARRERA_CHOICES = [
        ('INGENIERÍA INDUSTRIAL', 'Ingeniería Industrial'),
        ('INGENIERÍA INDUSTRIAL MIXTA', 'Ingeniería Industrial MIXTA'),
        ('INGENIERÍA EN GESTIÓN EMPRESARIAL', 'Ingeniería en Gestión Empresarial'),
        ('INGENIERÍA EN GESTIÓN EMPRESARIAL MIXTA', 'Ingeniería en Gestión Empresarial MIXTA'),
        ('INGENIERÍA EN SISTEMAS COMPUTACIONALES', 'Ingeniería en Sistemas Computacionales'),
        ('INGENIERÍA AMBIENTAL', 'Ingeniería Ambiental'),
        ('INGENIERÍA EN INDUSTRIAS ALIMENTARIAS', 'Ingeniería en Industrias Alimentarias'),
        ('INGENIERÍA EN AGRONOMÍA', 'Ingeniería en Agronomía'),
        ('INGENIERÍA EN INTELIGENCIA ARTIFICIAL', 'Ingeniería en Inteligencia Artificial'),
        ('INGENIERÍA EN DESARROLLO DE APLICACIONES', 'Ingeniería en Desarrollo de Aplicaciones'),
    ]
    
    # Relación de uno a uno con el modelo de usuario
    NoControl = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Campos adicionales para el perfil de alumno
    Nombre = models.CharField(max_length=70, blank=True, null=True)
    Apellidos = models.CharField(max_length=70, blank=True, null=True)
    Carrera = models.CharField(max_length=50, blank=True, null=True, choices=CARRERA_CHOICES)
    Fecha_nacimiento = models.DateField(null=True, blank=True)
    Genero = models.CharField(max_length=10, blank=True, null=True, choices=SEXO_CHOICES)
    Telefono = models.CharField(max_length=15, blank=True, null=True)
    Semestre = models.CharField(max_length=2, blank=True, null=True, choices=SEMESTRES_CHOICES)
    
    def __str__(self):
        return f"{self.Nombre} - {self.NoControl.username}"

class Empresas(models.Model):
    Nombre = models.CharField(max_length=50)
    Descripcion = models.TextField()
    Portada = models.ImageField()
    Logotipo = models.ImageField()

    def __str__(self):
        return self.Nombre
    
    def clean(self):
        if self.Portada:
            validar_tamano_imagen(self.Portada)
        if self.Logotipo:
            validar_tamano_imagen(self.Logotipo)


class Documento(models.Model):
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.titulo
    
    def clean(self):
        if self.archivo and self.archivo.size > 5 * 1024 * 1024:  # máximo 5MB
            raise ValidationError("El archivo PDF no puede superar los 5MB.")


class Convocatoria(models.Model):
    ESTADO_CHOICES = [
        ('Habilitada', 'Habilitada'),
        ('Deshabilitada', 'Deshabilitada')
    ]

    INGENIERIA_CHOICES = [
        ('INGENIERÍA INDUSTRIAL', 'Ingeniería Industrial'),
        ('INGENIERÍA INDUSTRIAL MIXTA', 'Ingeniería Industrial MIXTA'),
        ('INGENIERÍA EN GESTIÓN EMPRESARIAL', 'Ingeniería en Gestión Empresarial'),
        ('INGENIERÍA EN GESTIÓN EMPRESARIAL MIXTA', 'Ingeniería en Gestión Empresarial MIXTA'),
        ('INGENIERÍA EN SISTEMAS COMPUTACIONALES', 'Ingeniería en Sistemas Computacionales'),
        ('INGENIERÍA AMBIENTAL', 'Ingeniería Ambiental'),
        ('INGENIERÍA EN INDUSTRIAS ALIMENTARIAS', 'Ingeniería en Industrias Alimentarias'),
        ('INGENIERÍA EN AGRONOMÍA', 'Ingeniería en Agronomía'),
        ('INGENIERÍA EN INTELIGENCIA ARTIFICIAL', 'Ingeniería en Inteligencia Artificial'),
        ('INGENIERÍA EN DESARROLLO DE APLICACIONES', 'Ingeniería en Desarrollo de Aplicaciones'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    ingenierias = MultiSelectField(choices=INGENIERIA_CHOICES, blank=True)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    fecha_apertura = models.DateField()
    fecha_cierre = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Habilitada')
    puesto = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.empresa.Nombre}"
    

class Postulacion(models.Model):

    alumno = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE)
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aceptado', 'Aceptado'),
        ('Rechazado', 'Rechazado'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('alumno', 'convocatoria')

    def __str__(self):
        return f"{self.alumno} - {self.convocatoria} ({self.estado})"



class IngenieriaGaleria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    imagen_portada = models.ImageField(upload_to='ingenierias_portadas/', blank=True, null=True)
    imagen_logo = models.ImageField(upload_to='ingenierias_logo/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    
    def clean(self):
        if self.imagen_portada:
            validar_tamano_imagen(self.imagen_portada)
        if self.imagen_logo:
            validar_tamano_imagen(self.imagen_logo)


class Proyecto(models.Model):
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    ingenieria = models.ForeignKey(IngenieriaGaleria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.empresa.Nombre} - {self.ingenieria.nombre} - {self.nombre}"


class Evidencia(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='evidencias')
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='evidencias/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
    def clean(self):
        if self.imagen:
            validar_tamano_imagen(self.imagen)
    


class Index(models.Model):
    Titulo = models.CharField(max_length=100)
    Texto = models.TextField(blank=True, null=True)
    Imagen = models.ImageField(upload_to="index/")

    def __str__(self):
        return self.Titulo
    
    def clean(self):
        if self.Imagen:
            validar_tamano_imagen(self.Imagen)