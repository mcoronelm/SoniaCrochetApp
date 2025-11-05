from django.shortcuts import render, redirect
#Importar el formulario ContactoForm de forms.py
from .forms import ContactoForm


def contacto(request):
    #Verificar si el usuario envió el formulario
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        #Verificar que campos del formulario son válidos
        if form.is_valid():
            form.save()

            return redirect('Contacto')
    else:
        form = ContactoForm()

    return render(request, 'contacto.html', {'form': form})
