from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Ruta principal del panel (Dashboard) que el login está buscando con 'core:dashboard'
    path('', views.dashboard_view, name='dashboard'),
]