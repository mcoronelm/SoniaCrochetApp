from django.contrib import admin
from .models import Contacto

# Register your models here.

class ContactoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre","email", "mensaje", "created")
    readonly_fields = ("created",)


admin.site.register(Contacto, ContactoAdmin)
