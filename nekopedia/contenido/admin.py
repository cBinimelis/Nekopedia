from django.contrib import admin
from .models import Genero, Subgenero, ContenidoMultimedia, Temporada, Episodio


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ["nombre"]
    search_fields = ["nombre"]


@admin.register(Subgenero)
class SubgeneroAdmin(admin.ModelAdmin):
    list_display = ["nombre", "genero_principal"]
    list_filter = ["genero_principal"]
    search_fields = ["nombre"]


class TemporadaInline(admin.TabularInline):
    model = Temporada
    extra = 1


class EpisodioInline(admin.TabularInline):
    model = Episodio
    extra = 0
    fields = ["numero", "visto", "fecha_visto"]


@admin.register(ContenidoMultimedia)
class ContenidoMultimediaAdmin(admin.ModelAdmin):
    list_display = [
        "titulo",
        "tipo",
        "genero",
        "año_lanzamiento",
        "estado",
        "estado_visualizacion",
    ]
    list_filter = [
        "tipo",
        "genero",
        "estado",
        "estado_visualizacion",
        "año_lanzamiento",
    ]
    search_fields = ["titulo", "sinopsis"]
    filter_horizontal = ["subgeneros"]
    inlines = [TemporadaInline]

    fieldsets = (
        (
            "Información Básica",
            {"fields": ("tipo", "titulo", "sinopsis", "año_lanzamiento", "duracion")},
        ),
        ("Clasificación", {"fields": ("genero", "subgeneros")}),
        ("Estado", {"fields": ("estado", "estado_visualizacion")}),
        (
            "Información de Serie",
            {
                "fields": ("temporadas", "episodios_totales"),
                "classes": ("collapse",),
                "description": "Solo para series",
            },
        ),
        ("Imagen", {"fields": ("portada",)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("genero")


@admin.register(Temporada)
class TemporadaAdmin(admin.ModelAdmin):
    list_display = ["contenido", "numero", "nombre", "episodios"]
    list_filter = ["contenido"]
    inlines = [EpisodioInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("contenido")


@admin.register(Episodio)
class EpisodioAdmin(admin.ModelAdmin):
    list_display = ["temporada", "numero", "visto", "fecha_visto"]
    list_filter = ["visto", "temporada__contenido"]
    list_editable = ["visto"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("temporada__contenido")
