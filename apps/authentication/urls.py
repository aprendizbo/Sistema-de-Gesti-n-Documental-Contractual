from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Ruta para iniciar sesión (esta es la que soluciona el error NoReverseMatch)
    path('login/', views.login_view, name='login'),
    
    # Dejamos lista de una vez la ruta para cerrar sesión
    path('logout/', views.logout_view, name='logout'),
]