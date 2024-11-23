from django.db import models
from django.contrib.auth.models import User


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
    Correo_inst = models.EmailField(max_length=70, blank=True, null=True)
    Carrera = models.CharField(max_length=50, blank=True, null=True, choices=CARRERA_CHOICES)
    Fecha_nacimiento = models.DateField(null=True, blank=True)
    Genero = models.CharField(max_length=10, blank=True, null=True, choices=SEXO_CHOICES)
    Telefono = models.CharField(max_length=15, blank=True, null=True)
    Semestre = models.CharField(max_length=1, blank=True, null=True, choices=SEMESTRES_CHOICES)
    
    def __str__(self):
        return f"{self.Nombre} - {self.NoControl.username}"

class Empresas(models.Model):
    Nombre = models.CharField(max_length=50)
    Descripcion = models.TextField()
    Portada = models.ImageField()
    Logotipo = models.ImageField()

class Documento(models.Model):
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.titulo


