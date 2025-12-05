from django.db import models

TIPO = [
    ("ANIME", "Anime"),
    ("PELICULA", "Película"),
    ("SERIE", "Serie"),
    ("MANGA", "Manga"),
    ("LIBRO", "Libro"),
]

ESTADO = [
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
class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Géneros"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Contenido(models.Model):

    tipo = models.CharField(max_length=10, choices=TIPO)
    titulo = models.CharField(max_length=200,unique=True)
    titulo_alternativo =models.CharField(max_length=400,null=True, blank=True)
    sinopsis = models.TextField()
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    subgeneros = models.CharField(max_length=200)
    año_lanzamiento = models.PositiveIntegerField()
    
    #Campos Especificos 
    #Anime y Series
    temporadas = models.PositiveIntegerField(null=True, blank=True)
    episodios = models.PositiveIntegerField(help_text="Para series y anime", null=True, blank=True)
    
    #Peliculas
    duracion = models.PositiveIntegerField(help_text="Duración en minutos.")
    
    #Mangas
    tomos = models.PositiveIntegerField(null=True, blank=True)
    capitulos = models.PositiveIntegerField(help_text="Para mangas",null=True, blank=True)
    
    #Libros
    autor = models.CharField(max_length=100,null=True, blank=True)
    paginas = models.PositiveIntegerField(null=True, blank=True)
    saga = models.CharField(max_length=100,null=True, blank=True)
    
    # Estado del contenido
    estado = models.CharField(max_length=15, choices=ESTADO, default="COMPLETO")
    estado_visualizacion = models.CharField(max_length=15, choices=ESTADO_VISUALIZACION, default="PENDIENTE")

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
            self.episodios = None
            self.tomos = None
            self.capitulos = None
            self.autor = None
            self.paginas = None
            self.saga = None
        elif self.tipo =="SERIE" or self.tipo == "ANIME":
            self.duracion= None
            self.tomos = None
            self.capitulos = None
            self.autor = None
            self.paginas = None
            self.saga = None
        elif self.tipo == "MANGA":
            self.temporadas = None
            self.episodios = None
            self.duracion = None
            self.autor = None
            self.paginas = None
            self.saga = None
        elif self.tipo =="LIBRO":
            self.temporadas = None
            self.episodios = None
            self.tomos = None
            self.capitulos = None
            self.autor = None
            self.paginas = None
            self.saga = None
            
        super().save(*args, **kwargs)


""" 
class Episodio(models.Model):

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
"""