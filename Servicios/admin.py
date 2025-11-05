from django.contrib import admin
from .models import Servicio

# Register your models here.

class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id','titulo','contenido','imagen','created','update')
    #Poner campos de solo lectura
    readonly_fields = ('created', 'update')

admin.site.register(Servicio, ServicioAdmin)