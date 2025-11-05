from django.contrib import admin
from .models import Categoria, Post

# Register your models here.

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "created", "updated")
    readonly_fields = ("created", "updated")

class PostAdmin(admin.ModelAdmin):
    list_display = ("id","titulo","contenido","imagen","autor","created","updated")
    readonly_fields = ("created", "updated")

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Post, PostAdmin)
