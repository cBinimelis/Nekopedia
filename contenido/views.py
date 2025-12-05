from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Genero

def home(request):
    pass
"""

def listado_contenido(request):
    ""Vista principal con búsqueda y filtros""
    contenidos = ContenidoMultimedia.objects.all()

    # Búsqueda por título
    busqueda = request.GET.get("buscar", "")
    if busqueda:
        contenidos = contenidos.filter(
            Q(titulo__icontains=busqueda) | Q(sinopsis__icontains=busqueda)
        )

    # Filtro por tipo (película o serie)
    tipo = request.GET.get("tipo", "")
    if tipo:
        contenidos = contenidos.filter(tipo=tipo)

    # Filtro por género
    genero_id = request.GET.get("genero", "")
    if genero_id:
        contenidos = contenidos.filter(genero_id=genero_id)

    # Filtro por año
    año = request.GET.get("año", "")
    if año:
        contenidos = contenidos.filter(año_lanzamiento=año)

    # Filtro por estado de visualización
    estado_visual = request.GET.get("estado_visual", "")
    if estado_visual:
        contenidos = contenidos.filter(estado_visualizacion=estado_visual)

    # Ordenamiento
    orden = request.GET.get("orden", "-fecha_agregado")
    orden_opciones = {
        "titulo_asc": "titulo",
        "titulo_desc": "-titulo",
        "año_asc": "año_lanzamiento",
        "año_desc": "-año_lanzamiento",
        "reciente": "-fecha_agregado",
        "antiguo": "fecha_agregado",
    }
    if orden in orden_opciones:
        contenidos = contenidos.order_by(orden_opciones[orden])

    # Obtener datos para los filtros
    generos = Genero.objects.all()
    años_disponibles = (
        ContenidoMultimedia.objects.values_list("año_lanzamiento", flat=True)
        .distinct()
        .order_by("-año_lanzamiento")
    )

    context = {
        "contenidos": contenidos,
        "generos": generos,
        "años": años_disponibles,
        "busqueda": busqueda,
        "filtro_tipo": tipo,
        "filtro_genero": genero_id,
        "filtro_año": año,
        "filtro_estado": estado_visual,
        "orden_actual": orden,
    }

    return render(request, "contenido/listado.html", context)


def detalle_contenido(request, pk):
    ""Vista de detalle de un contenido""
    contenido = get_object_or_404(ContenidoMultimedia, pk=pk)

    # Si es una serie, obtener las temporadas y episodios
    temporadas = None
    if contenido.tipo == "SERIE":
        temporadas = contenido.temporadas_detalle.all().prefetch_related(
            "episodios_vistos"
        )

    context = {
        "contenido": contenido,
        "temporadas": temporadas,
    }

    return render(request, "contenido/detalle.html", context)
"""