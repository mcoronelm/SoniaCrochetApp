from django.db import models
from django.conf import settings
from Tienda.models import Producto
from decimal import Decimal

# Create your models here.

class Card(models.Model):
    cardholder = models.CharField(max_length=100)
    cardnumber = models.CharField(max_length=20)
    expirationDate = models.DateField()
    CVV = models.CharField(max_length=4)
    
class Cupon(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} ({self.porcentaje}%)"
    
class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    codigoDescuento = models.ForeignKey('Cupon', on_delete=models.SET_NULL, null=True, blank=True) # 👈 Referencia a Cupon
    finalizada = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'carrito'
        verbose_name_plural = 'carritos'

    def __str__(self):
        return f"Carrito de {self.usuario.username} ({'Finalizado' if self.finalizada else 'Activo'})"
    
    def subtotal(self):
        # Subtotal siempre devuelva un Decimal
        return sum(item.subtotal() for item in self.items.all())

    def total(self):
        """
        Calcula el total final aplicando Tax, Shipping (fijo) y el Descuento.
        """
        subtotal = self.subtotal()
        
        # Las constantes deben ser Decimal para compatibilidad
        tax = subtotal * Decimal('0.21')
        shipping = Decimal('5.00') # 👈 Usando la constante fija de 5.00
        descuento = Decimal('0')
    
        # Aplicar el descuento si existe y está activo
        if self.codigoDescuento and self.codigoDescuento.activo:
            descuento = subtotal * (self.codigoDescuento.porcentaje / Decimal('100'))

        total = subtotal + tax + shipping - descuento
        # Retorna el total redondeado a 2 decimales
        return round(total, 2)
        
class Item(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items') 
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

    def subtotal(self):
        return self.producto.precio * self.cantidad