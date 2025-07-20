from rest_framework import serializers
from bache.models import Bache, Localidad, Estado
from django.core.exceptions import ValidationError
from bache.models import Localidad, UPZ, Barrio
from PIL import Image
import io
from django.utils import timezone 
import random

class BarrioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barrio
        fields = ['id', 'nombre']

class UPZSerializer(serializers.ModelSerializer):
    barrios = BarrioSerializer(many=True, read_only=True)
    
    class Meta:
        model = UPZ
        fields = ['id', 'nombre', 'barrios']

class LocalidadSerializer(serializers.ModelSerializer):
    upzs = UPZSerializer(many=True, read_only=True)
    
    class Meta:
        model = Localidad
        fields = ['id', 'nombre', 'upzs']
           
class BacheSerializer(serializers.ModelSerializer):

    localidad = serializers.PrimaryKeyRelatedField(
        queryset=Localidad.objects.all(),
        required=True,
        error_messages={'required': 'La localidad es obligatoria'}
    )

    upz = serializers.PrimaryKeyRelatedField(
        queryset=UPZ.objects.all(),
        required=True,
        error_messages={'required': 'La UPZ es obligatoria'}
    )
    barrio = serializers.PrimaryKeyRelatedField(
        queryset=Barrio.objects.all(),
        required=True,
        error_messages={'required': 'El barrio es obligatorio'}
    )






    estado = serializers.ChoiceField(
        choices=Estado.choices,
        required=True,
        error_messages={'required': 'El estado es obligatorio'}
    )
    direccion = serializers.CharField(
        required=True,
        error_messages={'required': 'La dirección es obligatoria'}
    )
    diametro = serializers.DecimalField(
        max_digits=9, decimal_places=6,
        required=True,
        error_messages={'required': 'El diámetro es obligatorio'}
    )
    foto = serializers.ImageField(
        required=True,  # Campo obligatorio
        allow_null=False,  # No permitir nulo
        help_text='Suba una imagen JPG/PNG (máx. 2MB)',
        error_messages={
            'required': 'La foto es obligatoria',
            'null': 'La foto no puede ser nula'
        }
    )
    
     # Campos de solo lectura para mostrar nombres
    nombre_localidad = serializers.SerializerMethodField()
    nombre_upz = serializers.SerializerMethodField()
    nombre_barrio = serializers.SerializerMethodField()

    def get_nombre_localidad(self, obj):
        return obj.localidad.nombre if obj.localidad else None

    def get_nombre_upz(self, obj):
        return obj.upz.nombre if obj.upz else None

    def get_nombre_barrio(self, obj):
        return obj.barrio.nombre if obj.barrio else None
     
     # Campos de fecha/hora personalizados  
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True, allow_null=True)
    deleted_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True, allow_null=True)
    id_bache = serializers.CharField(read_only=True)  # Asegura que sea solo lectura

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['created_at']:
            data['created_at'] = timezone.localtime(instance.created_at).isoformat()
        return data

    class Meta:
        model = Bache
        fields = '__all__'
        read_only_fields = [f.name for f in Bache._meta.get_fields() 
                          if f.name not in ['localidad','accidentes', 'diametro', 'direccion', 
                                          'peligrosidad', 'estado', 'foto','tipo_calle']]
        #read_only_fields = ['id_bache', 'created_at', 'deleted_at']

    def validate_foto(self, value):
        """Validación robusta del archivo de imagen"""
        try:
            with Image.open(io.BytesIO(value.read())) as img:
                value.seek(0)  # Rebobinar el archivo
                
                if img.format not in ['JPEG', 'PNG']:
                    raise ValidationError('Solo se permiten imágenes JPG/PNG')
                
                # Validación de tamaño (2MB máximo)
                if value.size > 2 * 1024 * 1024:
                    raise ValidationError('El tamaño máximo permitido es 2MB')
                    
        except Exception as e:
            raise ValidationError('El archivo no es una imagen válida')
        
        return value
    def validate(self, data):
        # Genera latitud y longitud aleatorias si no están en los datos
        if 'latitud' not in data or 'longitud' not in data:
            raise serializers.ValidationError({
                'latitud': 'La latitud es requerida',
                'longitud': 'La longitud es requerida'
            })
        
        # Validar relaciones jerárquicas
        if data.get('upz') and data['upz'].localidad != data['localidad']:
            raise serializers.ValidationError({
                'upz': 'La UPZ no pertenece a la localidad seleccionada'
            })
            
        if data.get('barrio') and data['barrio'].upz != data['upz']:
            raise serializers.ValidationError({
                'barrio': 'El barrio no pertenece a la UPZ seleccionada'
            })
            
        return data
    
class BacheUpdateSerializer(serializers.ModelSerializer):
     class Meta(BacheSerializer.Meta):
        # Restringe escritura a solo estos campos
        read_only_fields = [f.name for f in Bache._meta.get_fields() 
                          if f.name not in ['accidentes', 'diametro', 'direccion', 
                                          'peligrosidad', 'estado', 'foto','tipo_calle']]