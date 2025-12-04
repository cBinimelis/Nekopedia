from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import os


def content_image_path(instance, filename):
    """Genera la ruta personalizada para las imágenes"""
    ext = filename.split(".")[-1]
    prefix = "p" if instance.tipo == "PELICULA" else "a"
    filename = f"{prefix}_{instance.id:05d}.{ext}"
    return os.path.join("portadas", filename)


class Genero(models.Model):
    """Modelo para los géneros principales"""

    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Géneros"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Subgenero(models.Model):
    """Modelo para los subgéneros"""

    nombre = models.CharField(max_length=50, unique=True)
    genero_principal = models.ForeignKey(
        Genero, on_delete=models.CASCADE, related_name="subgeneros"
    )

    class Meta:
        verbose_name_plural = "Subgéneros"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.genero_principal.nombre})"


class ContenidoMultimedia(models.Model):
    """Modelo base para películas y series anime"""

    TIPO_CHOICES = [
        ("PELICULA", "Película"),
        ("SERIE", "Serie"),
    ]

    ESTADO_CHOICES = [
        ("COMPLETO", "Completo"),
        ("EN_EMISION", "En emisión"),
        ("CANCELADO", "Cancelado"),
        ("PROXIMO", "Próximo"),
    ]

    ESTADO_VISUALIZACION = [
        ("PENDIENTE", "Pendiente"),
        ("VIENDO", "Actualmente viendo"),
        ("VISTO", "Visto"),
        ("EN_PAUSA", "En pausa"),
    ]

    # Campos básicos
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    sinopsis = models.TextField()
    año_lanzamiento = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    duracion = models.PositiveIntegerField(
        help_text="Duración en minutos (por episodio para series)"
    )

    # Relaciones
    genero = models.ForeignKey(
        Genero, on_delete=models.PROTECT, related_name="contenidos"
    )
    subgeneros = models.ManyToManyField(
        Subgenero, blank=True, related_name="contenidos"
    )

    # Estado del contenido
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default="COMPLETO")
    estado_visualizacion = models.CharField(
        max_length=15, choices=ESTADO_VISUALIZACION, default="PENDIENTE"
    )

    # Campos específicos para series
    temporadas = models.PositiveIntegerField(null=True, blank=True)
    episodios_totales = models.PositiveIntegerField(null=True, blank=True)

    # Imagen de portada
    portada = models.ImageField(upload_to=content_image_path, null=True, blank=True)

    # Metadatos
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    fecha_modificado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Contenidos Multimedia"
        ordering = ["-fecha_agregado"]

    def __str__(self):
        return f"{self.titulo} ({self.año_lanzamiento})"

    def save(self, *args, **kwargs):
        # Si es una película, limpia los campos de serie
        if self.tipo == "PELICULA":
            self.temporadas = None
            self.episodios_totales = None
        super().save(*args, **kwargs)

        # Renombrar la imagen después de guardar (cuando ya tenemos ID)
        if self.portada and not self.portada.name.startswith("portadas/"):
            old_path = self.portada.path
            self.portada.name = content_image_path(self, self.portada.name)
            new_path = self.portada.path

            # Mover el archivo si es necesario
            if old_path != new_path and os.path.exists(old_path):
                os.rename(old_path, new_path)
                super().save(update_fields=["portada"])


class Temporada(models.Model):
    """Modelo para las temporadas de una serie"""

    contenido = models.ForeignKey(
        ContenidoMultimedia,
        on_delete=models.CASCADE,
        related_name="temporadas_detalle",
        limit_choices_to={"tipo": "SERIE"},
    )
    numero = models.PositiveIntegerField()
    nombre = models.CharField(max_length=100, blank=True)
    episodios = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "Temporadas"
        ordering = ["contenido", "numero"]
        unique_together = ["contenido", "numero"]

    def __str__(self):
        return f"{self.contenido.titulo} - Temporada {self.numero}"


class Episodio(models.Model):
    """Modelo para registrar el progreso de episodios vistos"""

    temporada = models.ForeignKey(
        Temporada, on_delete=models.CASCADE, related_name="episodios_vistos"
    )
    numero = models.PositiveIntegerField()
    visto = models.BooleanField(default=False)
    fecha_visto = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Episodios"
        ordering = ["temporada", "numero"]
        unique_together = ["temporada", "numero"]

    def __str__(self):
        return f"{self.temporada.contenido.titulo} - T{self.temporada.numero}E{self.numero}"
