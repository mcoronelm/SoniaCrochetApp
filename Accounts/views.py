from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClientRegisterForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm


def register_client(request):
    if request.method == 'POST':
        #Recupera la informacion de POST
        form = ClientRegisterForm(request.POST)
        
        if form.is_valid():
            # Successful POST
            form.save()
            messages.success(request, "Cuenta creada correctamente.")
            return redirect('login')
        
    else:
        
        form = ClientRegisterForm()
        
    # Render for initial GET, or for failed POST
    return render(request, 'accounts/register.html', {'form': form})


def login(request):
    
    #Obtiene la url de destino si GET ixiste
    next_url = request.GET.get('next')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"¡Bienvenido de nuevo, {username}!")
                
                #Si existe una URL 'next' válida, redirigir allí.Si no, a ('Home').
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('Home') 
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Hay errores en el formulario.")

    else:
        # Se asegura que el formulario tenga acceso a 'next' para pasarlo después del POST
        form = AuthenticationForm()

    # Si hay (next_url), se envía a template para usarla en el formulario.
    return render(request, 'accounts/login.html', {'form': form, 'next_url': next_url})