from django.contrib import admin
from .models import User

# Register your models here.
class CardAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name","last_name","password","email","is_active","is_client", "is_admin")
    
admin.site.register(User,CardAdmin)