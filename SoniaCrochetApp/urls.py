from django.urls import path, include 
from . import views

# Para ver las imagenes insertadas
from django.conf import settings
from django.conf.urls.static import static

# rutas
urlpatterns = [
    path('', views.home, name="Home"),
    path('carrito/', include('Cart.urls', namespace='cart')),
]

# rutas para el media
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)