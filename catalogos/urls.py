from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_contenido, name='lista_contenido'),
    path('nuevo/', views.crear_contenido, name='crear_contenido'),
    path('editar/<int:pk>/', views.editar_contenido, name='editar_contenido'),
    path('eliminar/<int:pk>/', views.eliminar_contenido, name='eliminar_contenido'),
    path('detalle/<int:pk>/', views.detalle_contenido, name='detalle_contenido'), 
    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]