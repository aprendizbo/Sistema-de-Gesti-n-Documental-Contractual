from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    """
    Vista principal del panel corporativo (Dashboard).
    Requiere que el usuario haya iniciado sesión obligatoriamente.
    """
    return render(request, 'core/dashboard.html')