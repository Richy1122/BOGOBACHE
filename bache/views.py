import logging
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Bache, UPZ, Barrio, Localidad, Tipo_calle, Peligrosidad, Estado
from .serializers import BacheSerializer, BacheUpdateSerializer, UPZSerializer, BarrioSerializer
from .forms import BacheForm
from django.core.serializers import serialize
import json

logger = logging.getLogger(__name__)

# AJAX: carga de UPZs
def cargar_upzs(request):
    localidad_id = request.GET.get('localidad_id')
    upzs = UPZ.objects.filter(localidad_id=localidad_id).values('id', 'nombre')
    return JsonResponse(list(upzs), safe=False)

# AJAX: carga de Barrios
def cargar_barrios(request):
    upz_id = request.GET.get('upz_id')
    barrios = Barrio.objects.filter(upz_id=upz_id).values('id', 'nombre')
    return JsonResponse(list(barrios), safe=False)

# API
@api_view(['GET'])
def upzs_por_localidad(request, localidad_id):
    upzs = UPZ.objects.filter(localidad_id=localidad_id)
    serializer = UPZSerializer(upzs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def barrios_por_upz(request, upz_id):
    barrios = Barrio.objects.filter(upz_id=upz_id)
    serializer = BarrioSerializer(barrios, many=True)
    return Response(serializer.data)

# Página: mapa estático
def mapa_baches(request):
    baches = Bache.objects.all().values('id_bache', 'latitud', 'longitud', 'estado', 'peligrosidad')
    return render(request, 'mapa.html', {
        'baches': list(baches),
        'google_maps_api_key': 'TU_API_KEY_DE_GOOGLE_MAPS'
    })

# Página principal
def index(request):
    form = BacheForm()
    bache_creado = request.GET.get('bache_creado') == '1'

    if request.method == 'POST':
        form = BacheForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('crear_bache') + '?bache_creado=1')

    return render(request, 'index.html', {
        'form': form,
        'localidades': Localidad.objects.all(),
        'upzs': UPZ.objects.all(),
        'barrios': Barrio.objects.all(),
        'bache_creado': bache_creado
    })

# Vista para crear baches
def crear_bache(request):
    form = BacheForm()

    if request.method == 'POST':
        form = BacheForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('crear_bache') + '?bache_creado=1')

    return render(request, 'bache/crear_bache.html', {
        'form': form,
        'localidades': Localidad.objects.all(),
        'bache_creado': request.GET.get('bache_creado') == '1'
    })

# Vista de consulta con filtros (renderiza el HTML con el mapa y filtros)
def ver_filtrado_baches(request):
    baches = Bache.objects.all()

    localidad = request.GET.get('localidad')
    upz = request.GET.get('upz')
    barrio = request.GET.get('barrio')
    estado = request.GET.get('estado')
    peligrosidad = request.GET.get('peligrosidad')
    tipo_calle = request.GET.get('tipo_calle')
    accidentes_min = request.GET.get('accidentes_min')
    accidentes_max = request.GET.get('accidentes_max')
    diametro_min = request.GET.get('diametro_min')
    diametro_max = request.GET.get('diametro_max')

    if localidad:
        baches = baches.filter(localidad__nombre=localidad)
    if upz:
        baches = baches.filter(upz__nombre=upz)
    if barrio:
        baches = baches.filter(barrio__nombre=barrio)
    if estado:
        baches = baches.filter(estado=estado)
    if peligrosidad:
        baches = baches.filter(peligrosidad=peligrosidad)
    if tipo_calle:
        baches = baches.filter(tipo_calle=tipo_calle)
    if accidentes_min:
        baches = baches.filter(accidentes__gte=int(accidentes_min))
    if accidentes_max:
        baches = baches.filter(accidentes__lte=int(accidentes_max))
    if diametro_min:
        baches = baches.filter(diametro__gte=float(diametro_min))
    if diametro_max:
        baches = baches.filter(diametro__lte=float(diametro_max))

    baches_data = [
        {
            'id': b.id_bache,
            'lat': float(b.latitud),
            'lng': float(b.longitud),
            'direccion': b.direccion,
            'localidad': b.localidad.nombre if b.localidad else "",
            'upz': b.upz.nombre if b.upz else "",
            'barrio': b.barrio.nombre if b.barrio else "",
            'estado': b.estado,
            'peligrosidad': b.peligrosidad,
            'tipo_calle': b.tipo_calle,
            'accidentes': b.accidentes,
            'diametro': float(b.diametro)
        }
        for b in baches
    ]

    baches_json = json.dumps(baches_data)
    logger.warning(f"Baches serializados: {baches_json[:1000]}")

    context = {
        'baches_json': baches_json,
        'localidades': Localidad.objects.all(),
        'upzs': UPZ.objects.all(),
        'barrios': Barrio.objects.all(),
        'peligrosidades': Peligrosidad.choices,
        'tipos_calle': Tipo_calle.choices,
        'estados': Estado.choices
    }

    return render(request, 'bache/filtrar_baches.html', context)

@csrf_exempt
def filtrar_baches(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    baches = Bache.objects.all()

    localidad = data.get('localidad')
    upz = data.get('upz')
    barrio = data.get('barrio')
    estado = data.get('estado')
    peligrosidad = data.get('peligrosidad')
    tipo_calle = data.get('tipo_calle')
    accidentes = data.get('accidentes')
    diametro = data.get('diametro')

    if localidad:
        baches = baches.filter(localidad_id=localidad)
    if upz:
        baches = baches.filter(upz_id=upz)
    if barrio:
        baches = baches.filter(barrio_id=barrio)
    if estado:
        baches = baches.filter(estado=estado)
    if peligrosidad:
        baches = baches.filter(peligrosidad=peligrosidad)
    if tipo_calle:
        baches = baches.filter(tipo_calle=tipo_calle)
    if accidentes:
        try:
            baches = baches.filter(accidentes__gte=int(accidentes))
        except ValueError:
            pass
    if diametro:
        try:
            baches = baches.filter(diametro__gte=float(diametro))
        except ValueError:
            pass

    baches_data = []
    for b in baches:
        baches_data.append({
            'id_bache': b.id_bache,
            'latitud': float(b.latitud),
            'longitud': float(b.longitud),
            'direccion': b.direccion,
            'estado': b.estado,
            'peligrosidad': b.peligrosidad,
            'tipo_calle': b.tipo_calle,
            'accidentes': b.accidentes,
            'diametro': float(b.diametro),
            'foto': b.foto.url if b.foto else "",
            'localidad': b.localidad.nombre if b.localidad else "",
            'upz': b.upz.nombre if b.upz else "",
            'barrio': b.barrio.nombre if b.barrio else ""
        })

    return JsonResponse(baches_data, safe=False)

def obtener_filtros(request):
    localidades = list(Localidad.objects.values('id', 'nombre'))
    upzs = list(UPZ.objects.values('id', 'nombre', 'localidad_id'))
    barrios = list(Barrio.objects.values('id', 'nombre', 'upz_id'))
    tipos_calle = list(Bache.objects.values_list('tipo_calle', flat=True).distinct())
    estados = list(Bache.objects.values_list('estado', flat=True).distinct())
    niveles_peligrosidad = list(Bache.objects.values_list('peligrosidad', flat=True).distinct())

    max_accidentes = Bache.objects.all().order_by('-accidentes').first().accidentes if Bache.objects.exists() else 0
    max_diametro = Bache.objects.all().order_by('-diametro').first().diametro if Bache.objects.exists() else 0

    return JsonResponse({
        'localidades': localidades,
        'upzs': upzs,
        'barrios': barrios,
        'tipos_calle': tipos_calle,
        'estados': estados,
        'peligrosidad': niveles_peligrosidad,
        'max_accidentes': max_accidentes,
        'max_diametro': float(max_diametro),
    })

def somos(request):
    return render(request, 'somos.html', { 'title': 'PAGINA' })

def sesion(request):
    return render(request, 'somos.html', { 'title': 'PAGINA' })

class BacheViewSet(viewsets.ModelViewSet):
    queryset = Bache.objects.all()
    serializer_class = BacheSerializer
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return BacheUpdateSerializer
        return BacheSerializer

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            logger.debug(f"Actualizando bache {instance.id_bache} con datos: {request.data}")
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except Exception as e:
            logger.error(f"Error al actualizar bache: {str(e)}", exc_info=True)
            raise

        full_serializer = BacheSerializer(instance)
        return Response(full_serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        logger.info(f"Datos recibidos para crear bache: {request.data}")
        response = super().create(request, *args, **kwargs)
        logger.info(f"Bache creado con ID: {response.data.get('id_bache')}")
        return response


@api_view(['GET'])
def get_bache(request, id_bache):
    try:
        bache = get_object_or_404(Bache, id_bache=id_bache)
        data = {
            "id_bache": bache.id_bache,
            "localidad": bache.localidad.id if bache.localidad else None,
            "upz": bache.upz.id if bache.upz else None,
            "barrio": bache.barrio.id if bache.barrio else None,
            "peligrosidad": bache.peligrosidad,
            "estado": bache.estado,
            "tipo_calle": bache.tipo_calle.id if bache.tipo_calle else None,
            "direccion": bache.direccion,
            "accidentes": bache.accidentes,
            "diametro": float(bache.diametro),
            "latitud": float(bache.latitud),
            "longitud": float(bache.longitud),
            "foto": bache.foto.url if bache.foto else None,
        }
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_bache(request, id_bache):
    try:
        bache = get_object_or_404(Bache, id_bache=id_bache)
        data = {
            "id_bache": bache.id_bache,
            "localidad": bache.localidad.id if bache.localidad else None,
            "upz": bache.upz.id if bache.upz else None,
            "barrio": bache.barrio.id if bache.barrio else None,
            "peligrosidad": bache.peligrosidad,
            "estado": bache.estado,
            "tipo_calle": bache.tipo_calle,
            "direccion": bache.direccion,
            "accidentes": bache.accidentes,
            "diametro": float(bache.diametro),
            "latitud": float(bache.latitud),
            "longitud": float(bache.longitud),
            "foto": bache.foto.url if bache.foto else None,
        }
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@csrf_exempt
@require_http_methods(["POST"])
def modificar_bache_post(request, id_bache):
    try:
        data = json.loads(request.body.decode('utf-8'))

        bache = get_object_or_404(Bache, id_bache=id_bache)

        bache.estado = data.get('estado', bache.estado)
        bache.peligrosidad = data.get('peligrosidad', bache.peligrosidad)
        bache.tipo_calle_id = data.get('tipo_calle', bache.tipo_calle_id)
        bache.direccion = data.get('direccion', bache.direccion)
        bache.accidentes = data.get('accidentes', bache.accidentes)
        bache.diametro = data.get('diametro', bache.diametro)

        bache.save()
        return JsonResponse({'success': True, 'message': 'Bache actualizado correctamente.'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
@csrf_exempt
@require_http_methods(["GET", "POST"])
def modificar_bache(request):
    context = {
        'localidades': Localidad.objects.all(),
        'upzs': UPZ.objects.all(),
        'barrios': Barrio.objects.all(),
        'baches': Bache.objects.all(),
        'tipos_calle': Tipo_calle.objects.all()
    }

    if request.method == 'POST':
        id_bache = request.POST.get('id_bache')

        try:
            bache = Bache.objects.get(id_bache=id_bache)
            context['bache'] = bache
            context['id_bache'] = id_bache
        except Bache.DoesNotExist:
            context['error'] = f"No se encontró el bache con ID {id_bache}"

    return render(request, 'bache/modificar_bache.html', context)