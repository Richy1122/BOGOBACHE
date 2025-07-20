from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
# Create your models here.
class Peligrosidad(models.TextChoices):
    ALTO = "Alto"
    MEDIO = "Medio"
    BAJO = "Bajo"

class Estado(models.TextChoices):
    SIN_ARREGLAR = "sin_arreglar"
    EN_PROCESO = "en_proceso"
    ARREGLADO = "arreglado"

class Localidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

class UPZ(models.Model):
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE, related_name='upzs')
    nombre = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('localidad', 'nombre')  # Evita UPZs duplicadas en una localidad
    
    def __str__(self):
        return f"{self.nombre} ({self.localidad})"

class Barrio(models.Model):
    upz = models.ForeignKey(UPZ, on_delete=models.CASCADE, related_name='barrios')
    nombre = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('upz', 'nombre')  # Evita barrios duplicados en una UPZ
    
    def __str__(self):
        return f"{self.nombre} ({self.upz})"
    
class Tipo_calle(models.TextChoices):
    CALLES = "Calle"
    CARRERAS = "Carrera"
    AVENIDAS = "Avenida"
    TRANSVERSALES ="Transversal"
    Diagonales ="Diagonal"
    CALLEJONES = "Callejones"

class Bache(models.Model):
    #localidad = models.CharField(max_length=100, choices=Localidad.choices, default=Localidad.USAQUEN)
    # Modificar las relaciones para mejor consistencia
    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT, related_name='baches')
    upz = models.ForeignKey(UPZ, on_delete=models.PROTECT, related_name='baches')
    barrio = models.ForeignKey(Barrio, on_delete=models.PROTECT, related_name='baches')
    
    estado = models.CharField(max_length=100, choices=Estado.choices, default=Estado.SIN_ARREGLAR)

    peligrosidad = models.CharField(max_length=100, choices=Peligrosidad.choices, default=Peligrosidad.BAJO)

    tipo_calle = models.CharField(max_length=100, choices=Tipo_calle.choices, default=Tipo_calle.CALLES)

    direccion = models.CharField(max_length=100)

    latitud = models.DecimalField(max_digits=25, decimal_places=20, verbose_name='latitud', null=False, blank=False)

    longitud = models.DecimalField(max_digits=25, decimal_places=20, verbose_name='longitud', null=False, blank=False)

    diametro = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='diametro', null=False, blank=False)

    accidentes = models.PositiveIntegerField(default=0, null=False, blank=False)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


    foto = models.ImageField(
        upload_to='images/',
        verbose_name='Fotografía del incidente',
        help_text='Suba una imagen clara del accidente (Formatos permitidos: JPG, JPEG, PNG)',
        blank=False,  # No permitir en blanco
        null=False,   # No permitir nulo
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        ]
    )
    id_bache = models.CharField(
        max_length=8,
        unique=True,
        editable=False,
        verbose_name='ID del Bache',
        help_text='Identificador único con formato BHC seguido de 5 letras mayúsculas (excluyendo I y O)',
        primary_key=True
    )

    def generar_id_bache(self):
        """Genera un ID BHCXXXXX único con 5 letras aleatorias (excluyendo I y O)"""
        while True:
            letras_permitidas = 'ABCDEFGHJKLMNPQRSTUVWXYZ'  # Excluye I y O
            nuevo_id = 'BHC' + get_random_string(5, allowed_chars=letras_permitidas)
            if not Bache.objects.filter(id_bache=nuevo_id).exists():
                return nuevo_id

    def save(self, *args, **kwargs):
        """Genera automáticamente el ID al crear un nuevo registro"""
        if not self.id_bache:
            self.id_bache = self.generar_id_bache()
        super().save(*args, **kwargs)

    def clean(self):
        """Valida el formato del ID si se modifica manualmente (aunque editable=False lo previene)"""
        if self.id_bache and (len(self.id_bache) != 8 or 
                             not self.id_bache.startswith('BHC') or 
                             not self.id_bache[3:].isalpha() or
                             any(c in self.id_bache[3:] for c in 'IO')):
            raise ValidationError(
                "El ID debe tener formato BHC seguido de 5 letras mayúsculas (excluyendo I y O). Ejemplo: BHCQAZWS"
            )

    class Meta:
        verbose_name = 'Bache'
        verbose_name_plural = 'Baches'
        ordering = ['id_bache']

    def save(self, *args, **kwargs):
        """Genera automáticamente el ID al crear un nuevo registro"""
        if not self.id_bache:
            self.id_bache = self.generar_id_bache()
        if not self._state.adding:  # Solo si ya existe (actualización)
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if kwargs.pop('hard_delete', False):
            return super().delete(*args, **kwargs)
        self.deleted_at = timezone.now()
        self.save()
