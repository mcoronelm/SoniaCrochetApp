from django.db import models

# Create your models here.
class Color(models.Model):
    nombre = models.CharField(max_length=50)
    #Preguntar al profesor si es mejor hex o color
    hex = models.CharField(max_length=7)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'color'
        verbose_name_plural = 'colores'

    def __str__(self):
        return self.nombre
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    #atributos
    nombre = models.CharField(max_length=50)
    #max_digits=10 → número total de dígitos (antes + después del punto decimal)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='tienda')
    #Solo accede desde producto hacia colores y no viceversa
    colores = models.ManyToManyField(Color, verbose_name="Colores disponibles")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    oferta = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return self.nombre
