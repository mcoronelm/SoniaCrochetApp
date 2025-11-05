from django.urls import path 
from . import views 
 
# CRÍTICO: Define el namespace para que funcione la función 'include'
app_name = 'cart'

urlpatterns = [ 
    # Ruta principal del carrito (ej: /carrito/)
    path('', views.cart, name='Cart'), 
    
    # Añade un producto o incrementa su cantidad
    path('add/<int:producto_id>/', views.add_to_cart, name='add_to_cart'), 
    
    # Decrementa la cantidad de un producto
    path('restar/<int:producto_id>/', views.restar_producto, name='restar_producto'),
    
    # Actualiza la cantidad de un item (si es necesario)
    path('update-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'), 
    
    # Elimina un item del carrito
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'), 
    
    #aplica el descueno
    path('apply/', views.apply_coupon, name='apply_coupon'),
    
    #Finaliza el pago
    path('pago/finalizar/', views.process_payment, name='process_payment'),
    path('pagado/', views.pago_completado, name='pagado'),
]
