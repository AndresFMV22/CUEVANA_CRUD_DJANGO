from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class Contenido(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    anio = models.IntegerField(
        validators=[
            MinValueValidator(1888, message="El año no puede ser menor a 1888 (origen del cine)"),
            MaxValueValidator(datetime.now().year + 1, message=f"No se puede superar el año {datetime.now().year + 1}")
        ],
        help_text="Año de lanzamiento (entre 1888 y el año siguiente)"
    )
    genero = models.CharField(max_length=100)
    imagen_url = models.URLField(blank=True, null=True)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    video_url = models.URLField(blank=True, null=True, help_text="URL del tráiler o película (YouTube, Vimeo, etc.)")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Contenido"
        verbose_name_plural = "Contenidos"