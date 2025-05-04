# Plataforma Para La Gestión y Administración De Educación Dual

![Django](https://img.shields.io/badge/Django-4.x-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-Propietaria-lightgrey)
![Estado](https://img.shields.io/badge/Estado-En%20Desarrollo-orange)


Sistema web desarrollado con Django que permite la gestión de convocatorias, postulaciones y perfiles de estudiantes dentro del modelo de Educación Dual.

## 📋 Descripción

Esta plataforma facilita la administración de convocatorias y postulaciones para estudiantes interesados en integrarse al modelo de Educación Dual. Permite a los administradores crear y gestionar convocatorias y a los usuarios (estudiantes) registrarse, completar su perfil y postularse a las oportunidades disponibles.

## 🚀 Características principales

- Registro y autenticación de usuarios.
- Perfil de estudiantes con datos académicos y personales.
- Creación y gestión de convocatorias.
- Proceso de postulación a convocatorias.
- Panel de administración para la gestión de usuarios y contenido.
- Formularios personalizados para captura de datos.

## 🛠️ Tecnologías utilizadas

- **Backend:** Django 4+
- **Frontend:** HTML5, CSS3 (plantillas de Django)
- **Base de datos:** PostgreSQL
- **Otros:** 
  - Python 3.12+
  - Admin personalizado de Django
  - Git para control de versiones

## 🏗️ Estructura del proyecto

```

Servicio/
├── manage.py
├── Servicio/                  # Configuración general del proyecto
├── EducacionDual/             # App principal
│   ├── models.py              # Modelos de datos
│   ├── views.py               # Vistas
│   ├── urls.py                # Rutas
│   ├── forms.py               # Formularios
│   ├── admin.py               # Personalización del admin
│   ├── migrations/            # Migraciones de la base de datos
│   ├── templates/             # Plantillas HTML del Proyecto 
│   ├── static/                # Css/Js/img
├── requirements.txt           # Dependencias del proyecto
├── .gitignore

````

## ⚙️ Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Edgar2607821/Servicio.git
   cd Servicio


2. **Crear un entorno virtual e instalar dependencias**

   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Aplicar migraciones**

   ```bash
   python manage.py migrate
   ```

4. **Crear superusuario**

   ```bash
   python manage.py createsuperuser
   ```

5. **Ejecutar el servidor**

   ```bash
   python manage.py runserver
   ```

Accede a `http://127.0.0.1:8000` para ver la aplicación.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Puedes abrir issues para reportar problemas o sugerir mejoras. Para contribuir directamente, haz un fork del repositorio y crea un Pull Request.

Si deseas contribuir, sigue estos pasos:

1. **Abrir un Issue**
   - Si detectas un problema o tienes una sugerencia de mejora, abre un *issue* describiendo el problema o la propuesta.
   - Usa un título claro y proporciona toda la información necesaria para reproducir el problema (si aplica).

2. **Hacer un fork del repositorio**
   - Entra al repositorio principal y haz clic en el botón "Fork".
   - Esto creará una copia del proyecto en tu propia cuenta de GitHub.

3. **Clonar tu fork**
   ```bash
   git clone https://github.com/TU_USUARIO/TU_FORK.git
   cd NOMBRE_DEL_REPOSITORIO


4. **Crear una nueva rama para tu contribución**

   ```bash
   git checkout -b nombre-de-tu-rama
   ```

   Ejemplo:

   ```bash
   git checkout -b feature/estadisticas
   ```

5. **Realizar los cambios**

   * Haz los cambios necesarios en tu rama.
   * Asegúrate de seguir el mismo estilo de código que el resto del proyecto.
   * Prueba tus cambios localmente.

6. **Guardar y subir los cambios**

   ```bash
   git add .
   git commit -m "Descripción breve de los cambios"
   git push origin nombre-de-tu-rama
   ```

7. **Crear un Pull Request (PR)**

   * Ve a tu repositorio en GitHub.
   * Haz clic en "Compare & Pull Request".
   * Llena el formulario describiendo qué cambios realizaste y por qué.
   * Envía el Pull Request.

8. **Revisión**

   * El equipo de mantenimiento revisará tu PR.
   * Puede que te hagan comentarios o sugerencias antes de aceptar los cambios.

### 📝 Reglas básicas para contribuir

* Sigue las buenas prácticas de codificación (usa el mismo estilo del proyecto).
* Escribe commits claros y descriptivos.
* Si tienes dudas, pregunta antes de hacer cambios mayores.
* Sé respetuoso en la comunicación.

**¡No te preocupes si es tu primera vez contribuyendo!**
Puedes preguntar cualquier duda y te ayudaremos en el proceso.


## 📄 Licencia

Este proyecto está licenciado bajo los términos definidos por el autor. Por favor, contacta al responsable del proyecto para más detalles.

---

**Desarrollado por:** Ing. Edgar Balleza Hernández y Ing. Erick Daniel Herbert Rodríguez.

**Contacto:** *(Correo Personal (Edgar Balleza): edgarballeza87@gmail.com, Correo Institucional (Edgar Balleza): 21690104@tecvalles.mx, Correo Personal (Erick Daniel): erick45her@gmail.com, Correo Institucional (Erick Daniel): 21690100@tecvalles.mx)*.
