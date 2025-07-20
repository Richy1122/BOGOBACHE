import logging
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse, Http404

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
from django.views.decorators.http import require_POST

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
    baches = Bache.objects.filter(deleted_at__isnull=True).values('id_bache', 'latitud', 'longitud', 'estado', 'peligrosidad')
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
    baches = Bache.objects.filter(deleted_at__isnull=True)

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

    baches = Bache.objects.filter(deleted_at__isnull=True)

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

    max_accidentes = Bache.objects.filter(deleted_at__isnull=True).order_by('-accidentes').first().accidentes if Bache.objects.exists() else 0
    max_diametro = Bache.objects.filter(deleted_at__isnull=True).order_by('-diametro').first().diametro if Bache.objects.exists() else 0

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
    queryset = Bache.objects.filter(deleted_at__isnull=True)
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

@csrf_exempt
@require_http_methods(["GET"])
def mostrar_modificar_bache(request):
    """
    Vista que carga el HTML con el mapa y formulario de edición.
    No requiere ID al inicio.
    """
    context = {
        'localidades': Localidad.objects.all(),
        'tipos_calle': list(Tipo_calle.choices),
        'estados': list(Estado.choices),
        'peligrosidades': list(Peligrosidad.choices),
    }
    return render(request, 'bache/modificar_bache.html', context)


@csrf_exempt
@require_http_methods(["GET"])
def get_bache(request, id_bache):
    """
    API que retorna los datos del bache a modificar (por ID).
    """
    try:
        bache = get_object_or_404(Bache, id_bache=id_bache)
        data = {
            "id_bache": bache.id_bache,
            "localidad": {
                "id": bache.localidad.id,
                "nombre": bache.localidad.nombre,
            } if bache.localidad else None,
            "upz": {
                "id": bache.upz.id,
                "nombre": bache.upz.nombre,
            } if bache.upz else None,
            "barrio": {
                "id": bache.barrio.id,
                "nombre": bache.barrio.nombre,
            } if bache.barrio else None,
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
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error al obtener bache {id_bache}: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def modificar_bache_post(request, id_bache):
    """
    POST para actualizar un bache con datos + foto.
    """
    try:
        bache = get_object_or_404(Bache, id_bache=id_bache)

        estado = request.POST.get('estado')
        peligrosidad = request.POST.get('peligrosidad')
        tipo_calle = request.POST.get('tipo_calle')
        direccion = request.POST.get('direccion')
        accidentes = request.POST.get('accidentes')
        diametro = request.POST.get('diametro')

        bache.estado = estado or bache.estado
        bache.peligrosidad = peligrosidad or bache.peligrosidad
        bache.tipo_calle = tipo_calle or bache.tipo_calle
        bache.direccion = direccion or bache.direccion
        bache.accidentes = accidentes or bache.accidentes
        bache.diametro = diametro or bache.diametro

        if 'foto' in request.FILES:
            bache.foto = request.FILES['foto']

        bache.save()
        return JsonResponse({'success': True, 'message': 'Bache actualizado correctamente'})
    except Exception as e:
        logger.error(f"Error al actualizar bache: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def buscar_bache_eliminar(request):
    id_bache = request.GET.get('id_bache')
    try:
        bache = Bache.objects.get(id_bache=id_bache)
        data = {
            'localidad': bache.localidad,
            'upz': bache.upz.nombre,
            'barrio': bache.barrio.nombre,
            'estado': bache.estado,
            'peligrosidad': bache.peligrosidad,
            'tipo_calle': bache.tipo_calle,
            'direccion': bache.direccion,
            'accidentes': bache.accidentes,
            'diametro': bache.diametro,
            'latitud': bache.latitud,
            'longitud': bache.longitud,
            'foto': bache.foto.url if bache.foto else ''
        }
        return JsonResponse({'success': True, 'bache': data})
    except Bache.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'El bache no existe'})
    
@csrf_exempt
def mostrar_eliminar_bache(request):
    if request.method == 'POST':
        id_bache = request.POST.get('id_bache')
        try:
            bache = Bache.objects.get(id_bache=id_bache)
            bache.delete()
            return JsonResponse({'success': True, 'message': 'Bache eliminado correctamente'})
        except Bache.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El bache no existe'})
    return render(request, 'bache/eliminar_bache.html')


@require_POST
@csrf_exempt  # si no estás usando el decorador CSRF token en la plantilla
def eliminar_bache_confirmar(request, id):
    if request.method == "POST":
        try:
            bache = Bache.objects.get(pk=id)
            bache.delete()
            return JsonResponse({"success": True})
        except Bache.DoesNotExist:
            return JsonResponse({"success": False, "error": "Bache no encontrado"})
    return JsonResponse({"success": False, "error": "Método no permitido"})

def mostrar_registrar_accidente(request):
    return render(request, 'bache/registrar_accidente.html')


def admin_eliminar_bache_directo(request, id_bache):
    if request.method == 'POST':
        try:
            bache = Bache.objects.get(id_bache=id_bache)
            bache.delete(hard_delete=True)  # esto borra realmente
            return JsonResponse({'success': True})
        except Bache.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Bache no encontrado'})
    else:
        raise Http404("Método no permitido")
    
def api_registrar_accidente(request, id_bache):
    if request.method == 'POST':
        try:
            bache = get_object_or_404(Bache, id_bache=id_bache)
            bache.accidentes += 1
            bache.save()
            return JsonResponse({'status': 'success', 'message': 'Accidente registrado correctamente.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})