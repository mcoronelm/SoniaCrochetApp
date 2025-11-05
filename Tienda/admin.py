from django.contrib import admin
from .models import Color, Categoria, Producto

# Register your models here.

class ColorAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre","hex", "created", "updated")
    readonly_fields = ("created", "updated")

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id","nombre","created","updated")
    readonly_fields = ("created", "updated")

class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id","nombre","precio","imagen","categoria","oferta","created", "updated")
    readonly_fields = ("created", "updated")


admin.site.register(Color,ColorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
