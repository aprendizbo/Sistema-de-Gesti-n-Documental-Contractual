from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard') # Redirige si ya tiene sesión

    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'authentication/login.html')

def logout_view(request):
    logout(request)
    return redirect('authentication:login')