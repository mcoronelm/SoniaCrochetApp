from django.db import models

# Create your models here.

#Guardar los datos del formulario
class Contacto(models.Model):
    #inputs del formulario
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'contacto'
        verbose_name_plural = 'contactos'

    def __str__(self):
        return self.nombre