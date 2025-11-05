from django.contrib import admin
from .models import Card,Cupon,Carrito,Item

# Register your models here.
class CardAdmin(admin.ModelAdmin):
    list_display = ("id", "cardholder", "cardnumber", "expirationDate","CVV")
    
class CuponAdmin(admin.ModelAdmin):
    list_display = ("id", "codigo", "porcentaje", "activo")
    
class CarritoAdmin(admin.ModelAdmin):
    list_display = ("id","usuario","card","created","updated", "codigoDescuento","finalizada","subtotal","total")
    readonly_fields = ("created", "updated")
    
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "carrito", "producto", "cantidad")
    
    
admin.site.register(Card, CardAdmin)
admin.site.register(Cupon, CuponAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(Item, ItemAdmin)