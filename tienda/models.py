from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    imagen = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

# Señal para crear o actualizar el perfil de usuario
@receiver(post_save, sender=User)
def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
    # Solo crear el perfil si el usuario es nuevo y aún no tiene un perfil
    if created and not Perfil.objects.filter(user=instance).exists():
        Perfil.objects.create(user=instance)

class Reseña(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="reseñas")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    valoracion = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # Rango de 1 a 5 estrellas
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reseña de {self.usuario.username} para {self.producto.nombre}'
