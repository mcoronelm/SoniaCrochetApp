from decimal import Decimal 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model 
from django.contrib import messages
from django.db import transaction # Recomendado para operaciones de pago
from datetime import date # Necesario para validar la fecha de expiración
from django.utils import timezone 

from Tienda.models import Producto
# Objetos
from .models import Carrito, Item, Cupon, Card


User = get_user_model() 

# --- DESCUENTO ---
@login_required
def apply_coupon(request):
    """
    Procesa el código de descuento enviado por el usuario y lo aplica al carrito.
    """
    # Obtener el carrito activo
    try:
        carrito_activo = Carrito.objects.get(
            usuario=request.user, 
            finalizada=False
        )
    except Carrito.DoesNotExist:
        messages.error(request, "No tienes un carrito activo.")
        return redirect('cart:Cart')

    # Procesar el formulario POST
    if request.method == 'POST':
        # ⚠️ IMPORTANTE: El nombre del campo del formulario debe ser 'coupon_code'
        coupon_code = request.POST.get('coupon_code', '').strip().upper()

        # Si el usuario quiere quitar el cupon
        if not coupon_code:
            if carrito_activo.codigoDescuento:
                messages.info(request, f"El cupón '{carrito_activo.codigoDescuento.codigo}' ha sido retirado.")
            else:
                 messages.info(request, "No había un cupón activo para retirar.")
            
            carrito_activo.codigoDescuento = None
            carrito_activo.save()
            return redirect('cart:Cart')

        try:
            #Buscar y validar el cupón
            descuento = Cupon.objects.get(
                codigo=coupon_code,
                activo=True,
            )
            
            # Aplicar el cupón
            carrito_activo.codigoDescuento = descuento
            carrito_activo.save()
            messages.success(request, f"Cupón '{descuento.codigo}' aplicado con éxito. ¡Ahorras un {descuento.porcentaje}%!")

        except Cupon.DoesNotExist:
            # Si el cupón no existe o no es válido
            carrito_activo.codigoDescuento = None
            carrito_activo.save()
            messages.error(request, "Código de descuento inválido o inactivo.")
        
    return redirect('cart:Cart')

# --- MOSTRAR CARRITO  ---

@login_required
def cart(request):
    """
    Muestra el carrito actual del usuario y calcula los montos.
    """
    carrito_activo = Carrito.objects.filter(
        usuario = request.user,
        finalizada=False
    ).first()

    # Usamos el carrito para calcular los valores si existe el carrito
    if carrito_activo:
        items = carrito_activo.items.all()
        subtotal = carrito_activo.subtotal()
        
        # Calcular el monto de descuento por separado para mostrarlo
        descuento_monto = Decimal('0.00')
        if carrito_activo.codigoDescuento and carrito_activo.codigoDescuento.activo:
            porcentaje_descuento = carrito_activo.codigoDescuento.porcentaje / Decimal('100')
            descuento_monto = subtotal * porcentaje_descuento
            
        # Calcula Tax y Shipping (sin descuento)
        tax = subtotal * Decimal('0.21') 
        shipping = Decimal('5.00') 
        
        # El total ya incluye el descuento
        total = carrito_activo.total() 
    else:
        items = []
        subtotal = Decimal('0.00')
        tax = Decimal('0.00')
        shipping = Decimal('0.00')
        total = Decimal('0.00')
        descuento_monto = Decimal('0.00')

    context = {
        'carrito': carrito_activo,
        'items': items,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'descuento_monto': descuento_monto,
        'total': total,
    }

    return render(request, 'cart.html', context)


# --- Funciones del carrito ---

@login_required
def add_to_cart(request, producto_id):
    """Agregar un producto"""
    producto = get_object_or_404(Producto, id=producto_id)
    user_instance = request.user 

    try:
        cantidad = max(1, int(request.POST.get('cantidad', 1)))
    except ValueError:
        cantidad = 1

    carrito, _ = Carrito.objects.get_or_create(
        usuario=user_instance, 
        finalizada=False
    )

    item, created = Item.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': cantidad}
    )

    if not created:
        item.cantidad += cantidad
        item.save()

    return redirect('cart:Cart')

@login_required
def restar_producto(request, producto_id):
    """Quitar un Item"""
    try:
        carrito_activo = Carrito.objects.get(
            usuario=request.user, 
            finalizada=False
        )
    except Carrito.DoesNotExist:
        return redirect('cart:Cart')
    
    item = get_object_or_404(
        Item, 
        carrito=carrito_activo, 
        producto_id=producto_id
    )

    item.cantidad -= 1
    
    if item.cantidad <= 0:
        item.delete()
    else:
        item.save()
        
    return redirect('cart:Cart')

@login_required
def update_cart_item(request, item_id):
    """Modificar la cantidad de un producto en el carrito."""
    item = get_object_or_404(
        Item,
        id=item_id,
        carrito__usuario=request.user,
        carrito__finalizada=False
    )

    try:
        cantidad = int(request.POST.get('cantidad', 0))
    except ValueError:
        return redirect('cart:Cart') 

    if cantidad <= 0:
        item.delete()
    else:
        item.cantidad = cantidad
        item.save()

    return redirect('cart:Cart')

@login_required
def remove_from_cart(request, item_id):
    """Eliminar un producto """
    item = get_object_or_404(
        Item,
        id=item_id,
        carrito__usuario=request.user,
        carrito__finalizada=False
    )
    item.delete()
    return redirect('cart:Cart')

@login_required
def process_payment(request):
    """Procesar los datos de la tarjeta, validar y finalizar la compra."""
    if request.method == 'POST':
        #Capturar y limpiar datos del POST
        cardholder = request.POST.get('cardholder-name')
        # Limpiar espacios del número de tarjeta
        card_number = request.POST.get('card-number', '').replace(' ', '')
        month = request.POST.get('month')
        year = request.POST.get('year')
        cvv = request.POST.get('cvv')

        errors = {}
        
        # Validar nombre del titular
        if not cardholder or len(cardholder) < 3:
            errors['cardholder'] = "Ingrese un nombre válido."

        # Validar número de tarjeta (número aproximado de dígitos)
        if not (13 <= len(card_number) <= 16 and card_number.isdigit()):
             errors['card_number'] = "Número de tarjeta no válido."
        
        # Validar CVV (3 a 4)
        if not (3 <= len(cvv) <= 4 and cvv.isdigit()):
            errors['cvv'] = "CVV no válido."

        # Validar fecha de expiración
        try:
            full_year = 2000 + int(year) 
            exp_month = int(month)
            
            today = date.today()
            
            # Verifica si la tarjeta ha expirado
            if full_year < today.year or (full_year == today.year and exp_month < today.month):
                errors['expire_date'] = "La tarjeta ha expirado."
            
            #date: para guardar en el modelo Card 
            expiry_date_obj = date(full_year, exp_month, 1)

        except (ValueError, TypeError):
            errors['expire_date'] = "Fecha de expiración no válida."

        if not errors:
            try:
                # Asegurar que todo el proceso se complete
                with transaction.atomic():
                    #Crear la Card en la base de datos
                    card_obj = Card.objects.create(
                        cardholder=cardholder,
                        cardnumber=card_number,
                        expirationDate=expiry_date_obj,
                        CVV=cvv
                    )

                    #Finalizar el carrito activo
                    carrito_activo = Carrito.objects.get(
                        usuario=request.user, 
                        finalizada=False
                    )
                    
                    if carrito_activo.items.count() == 0:
                         messages.error(request, 'El carrito está vacío.')
                         return redirect('cart:Cart')

                    carrito_activo.card = card_obj
                    carrito_activo.finalizada = True
                    carrito_activo.save()

                    # Redirigir a la página de pago exitoso
                    messages.success(request, '¡Pago realizado con éxito! Tu pedido está en camino.')
                    return redirect('pagado')

            except Carrito.DoesNotExist:
                messages.error(request, 'No se encontró un carrito activo. No se pudo procesar el pago.')
            except Exception as e:
                # Atajar errores 
                messages.error(request, f'Ocurrió un error inesperado al procesar el pago: {e}')
                
            # Si hay un error en el try/except, volvemos a mostrar el carrito
            return redirect('cart:Cart')

        else:
            # Fallo de validación: 
            for error_msg in errors.values():
                messages.error(request, f'Error de pago: {error_msg}')
            
            return redirect('cart:Cart')

    return redirect('cart:Cart')

@login_required
def pago_completado(request):
    """
    Vista simple para renderizar la plantilla de pago exitoso.
    """
    return render(request, 'pagado.html')