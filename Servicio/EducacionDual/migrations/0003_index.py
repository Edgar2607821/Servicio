# Generated by Django 5.1.2 on 2025-05-09 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EducacionDual', '0002_ingenieriagaleria_proyecto_evidencia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Titulo', models.CharField(max_length=100)),
                ('Texto', models.TextField(blank=True, null=True)),
                ('Imagen', models.ImageField(upload_to='index/')),
            ],
        ),
    ]
