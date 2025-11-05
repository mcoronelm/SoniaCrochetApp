from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from Tienda.models import Producto 


# Create your views here.

def home(request):
    # Recuperamos los primeros 3 productos
    productos_coleccion = Producto.objects.all()[:3] 
    
    # Creamos un contexto con los productos
    context = {
        'productos_coleccion': productos_coleccion,
    }
    
    # Renderizamos la plantilla con el contexto
    return render(request, 'SoniaCrochetApp/home.html', context)

