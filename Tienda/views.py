from django.shortcuts import render
from .models import Producto, Categoria, Color 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from Cart.models import *


# Create your views here.

def tienda(request):
    categorias = Categoria.objects.all()
    colores = Color.objects.all()
    productos = Producto.objects.all()
    return render(request, "tienda.html",{"productos":productos, "colores": colores, "categorias":categorias})

def categoria(request, categoria_id):
    categoria_obj = Categoria.objects.get(id=categoria_id)
    productos = Producto.objects.filter(categorias = categoria_obj)
    return render(request, "categorias.html", {"categoria": categoria_obj, "productos": productos})

def color(request, color_id):
    color_obj = Color.objects.get(id=color_id)
    productos = Producto.objects.filter(colores = color_obj)
    return render(request, "categorias.html", {"color": color_obj, "productos": productos})


@login_required 
def add_to_cart(request, product_id):
    # Obtener el producto o lanzar 404 si no existe
    product = get_object_or_404(Producto, id=Producto_id)
    
    # Obtener o crear el carrito para el usuario actual
    # OneToOneField: habrá un carrito por usuario.
    cart, created = Carrito.objects.get_or_create(user=request.user)
    
    # 3. Verificar si el producto ya está en el carrito
    try:
        # Si existe, actualiza la cantidad
        cart_item = Carrito.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Se agregó otra unidad de {product.name} al carrito.")
        
    except Item.DoesNotExist:
        # Si no existe, crea un nuevo CartItem con cantidad 1
        Item.objects.create(cart=cart, product=product, quantity=1)
        messages.success(request, f"¡{product.name} ha sido agregado al carrito!")

    # 4. Redirigir al usuario a la página de detalles del carrito
    # Asume que tienes una URL con name='cart_detail'
    return redirect('cart_detail')
