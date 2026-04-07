Cuevana CRUD - Plataforma de Gestión de Películas

> Proyecto universitario de **5to semestre – Plataformas de Programación**.
> Aplicación web desarrollada con **Django** que implementa un **CRUD completo** para un catálogo de películas y series, con autenticación por roles, filtros por género, tráilers de YouTube y una interfaz inspirada en **Cuevana**.

---

##  Características principales

* **CRUD completo** de películas/series
*  **Autenticación por roles**

  * Administradores
  * Usuarios normales
*  **Filtro por género**
*  **Reproducción de tráilers de YouTube**
*  **Interfaz moderna estilo Cuevana**
   **Diseño responsive**
*  **Base de datos en Supabase (PostgreSQL)**
*  **Permisos por grupos con Django Auth**

---

##  Tecnologías utilizadas

| Área          | Tecnología                              |
| ------------- | --------------------------------------- |
| Backend       | Django 4+ (Python)                      |
| Base de datos | Supabase + PostgreSQL                   |
| Frontend      | HTML5 + CSS3 puro                       |
| Diseño        | Glassmorphism + Gradientes + Responsive |
| Autenticación | Django Auth + Groups                    |
| Video         | YouTube Embed                           |
| Versionado    | Git + GitHub                            |

---

##  Estructura del proyecto

```bash
cuevana_crud/
├── catalogos/
│   ├── migrations/
│   ├── templates/catalogos/
│   │   ├── base.html
│   │   ├── lista.html
│   │   ├── detalle.html
│   │   ├── formulario.html
│   │   ├── confirmar_eliminar.html
│   │   ├── login.html
│   │   └── registro.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── context_processors.py
│
├── cuevana_crud/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/
├── .env
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

#  Explicación detallada de archivos clave

##  `models.py` – Modelo de datos

Define la tabla principal **Contenido**.

### Campos

* `titulo` → Nombre de la película o serie
* `descripcion` → Sinopsis
* `anio` → Año de lanzamiento
* `genero` → Género cinematográfico
* `imagen_url` → URL del póster
* `video_url` → URL del tráiler
* `fecha_agregado` → Fecha automática

###  Validaciones

* No permite años menores a **1888**
* No permite años negativos
* No permite fechas futuras más allá del próximo año

---

##  `views.py` – Lógica del sistema

Aquí se controla toda la lógica de negocio del CRUD.

| Función              | Método     | Descripción                         |
| -------------------- | ---------- | ----------------------------------- |
| `lista_contenido`    | GET        | Lista catálogo + filtro por género  |
| `crear_contenido`    | GET / POST | Crear contenido (solo admin)        |
| `editar_contenido`   | GET / POST | Editar contenido (solo admin)       |
| `eliminar_contenido` | GET / POST | Eliminar contenido con confirmación |
| `detalle_contenido`  | GET        | Ver detalle + tráiler               |
| `registro`           | GET / POST | Registro de usuarios                |
| `login_view`         | GET / POST | Inicio de sesión                    |
| `logout_view`        | GET        | Cierre de sesión                    |

###  Seguridad

```python
@user_passes_test(es_admin)
@login_required
```

Se usan decoradores para proteger las vistas administrativas.

---

##  `urls.py` – Rutas

```python
urlpatterns = [
    path('', views.lista_contenido, name='lista_contenido'),
    path('nuevo/', views.crear_contenido, name='crear_contenido'),
    path('editar/<int:pk>/', views.editar_contenido, name='editar_contenido'),
    path('eliminar/<int:pk>/', views.eliminar_contenido, name='eliminar_contenido'),
    path('detalle/<int:pk>/', views.detalle_contenido, name='detalle_contenido'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
```

---

##  Templates principales

### `base.html`

* Navbar dinámica
* Footer
* Estilos globales
* Diseño oscuro tipo streaming
* Botón **Nuevo contenido** visible solo para administradores

### `lista.html`

* Tarjetas del catálogo
* Filtros por género
* Botón de tráiler
* Opciones editar/eliminar según rol

### `detalle.html`

* Póster
* Descripción
* Año
* Género
* Tráiler embebido

### `formulario.html`

* Formulario de crear/editar
* Select dinámico de años
* Diseño glass

### `confirmar_eliminar.html`

* Confirmación antes del borrado

### `login.html` / `registro.html`

* Formularios de acceso
* Diseño consistente con toda la app

---

##  `context_processors.py`

Crea la variable global:

```python
es_admin
```

Disponible automáticamente en todos los templates.

---

##  Configuración (`settings.py`)

Incluye:

* Conexión con **Supabase**
* Variables de entorno con `.env`
* Redirecciones de login/logout
* Política segura para embeds de YouTube

```python
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
```

---

##  Variables de entorno

Archivo `.env`:

```env
SUPABASE_DB_URL=postgresql://usuario:password@host:5432/postgres
```

>  **Nunca subir este archivo a GitHub**

---

#  Roles y permisos

##  Administrador

Puede:

* Crear contenido
* Editar contenido
* Eliminar contenido
* Ver tráilers

##  Usuario normal

Puede:

* Ver catálogo
* Ver tráilers si inició sesión

##  Visitante

Puede:

* Ver catálogo
* No puede reproducir tráiler
* No puede editar

---

#  Instalación y puesta en marcha

##  Requisitos

* Python 3.8+
* Git
* Cuenta en Supabase

---

##  1) Clonar repositorio

```bash
git clone https://github.com/tuusuario/cuevana-crud-django.git
cd cuevana-crud-django
```

##  2) Crear entorno virtual

```bash
python -m venv venv
```

### Activar en Windows

```bash
venv\Scripts\activate
```

### Activar en Linux/Mac

```bash
source venv/bin/activate
```

##  3) Instalar dependencias

```bash
pip install -r requirements.txt
```

##  4) Configurar `.env`

```env
SUPABASE_DB_URL=postgresql://usuario:password@host:5432/postgres
```

##  5) Aplicar migraciones

```bash
python manage.py migrate
```

##  6) Crear grupos y permisos

```bash
python manage.py shell
```

Dentro de la shell:

```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalogos.models import Contenido

content_type = ContentType.objects.get_for_model(Contenido)
perm_add = Permission.objects.get(codename='add_contenido', content_type=content_type)
perm_change = Permission.objects.get(codename='change_contenido', content_type=content_type)
perm_delete = Permission.objects.get(codename='delete_contenido', content_type=content_type)

admin_group, _ = Group.objects.get_or_create(name='Administradores')
admin_group.permissions.add(perm_add, perm_change, perm_delete)

users_group, _ = Group.objects.get_or_create(name='Usuarios')
exit()
```

##  7) Crear superusuario

```bash
python manage.py createsuperuser
```

##  8) Ejecutar servidor

```bash
python manage.py runserver
```

Abrir en navegador:

```bash
http://127.0.0.1:8000
```

---

#  Uso de la aplicación

*  Registro / Login desde navbar
*  Ver catálogo público
*  Ver tráiler solo autenticados
*  Nuevo contenido solo admin
*  Editar / 🗑️ eliminar solo admin
*  Filtro por género

---

#  Manejo de videos de YouTube

Formatos soportados:

```text
https://www.youtube.com/watch?v=ID
https://youtu.be/ID
https://www.youtube.com/embed/ID
```

El sistema extrae automáticamente el **ID del video** y genera un `iframe` responsivo.

---

#  Comandos útiles

| Comando                            | Descripción            |
| ---------------------------------- | ---------------------- |
| `python manage.py runserver`       | Inicia servidor        |
| `python manage.py makemigrations`  | Crea migraciones       |
| `python manage.py migrate`         | Aplica migraciones     |
| `python manage.py createsuperuser` | Crea admin             |
| `python manage.py shell`           | Consola Django         |
| `pip freeze > requirements.txt`    | Actualiza dependencias |

---

#  Autores

* **Andres Martinez** → Backend, autenticación, CRUD, Supabase
* **Santiago Jaramillo** → Frontend, CSS, filtros, integración de videos

 Proyecto entregado para la asignatura **Plataformas de Programación – 5to semestre**.

---

#  Licencia

Proyecto de **uso académico**.

No se permite la reproducción total o parcial sin autorización de los autores.

---

#  Vista general del proyecto

Este proyecto busca simular una plataforma tipo **Cuevana / Netflix**, aplicando conceptos de:

* Django CRUD
* Roles y permisos
* Integración con servicios externos
* PostgreSQL en la nube
* UI/UX moderna con CSS puro

Ideal para portafolio universitario y presentación profesional en GitHub 
