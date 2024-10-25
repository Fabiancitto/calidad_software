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

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
    if created:
        # Se crea el perfil cuando se crea un nuevo usuario
        Perfil.objects.create(user=instance)
    else:
        # Asegúrate de que si se guarda un usuario, el perfil se mantenga actualizado
        try:
            instance.perfil.save()
        except Perfil.DoesNotExist:
            # Si no existe el perfil, se crea automáticamente
            Perfil.objects.create(user=instance)
