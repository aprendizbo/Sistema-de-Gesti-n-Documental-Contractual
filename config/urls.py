"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.urls import path, include

urlpatterns = [
    # El panel administrativo por defecto de Django ha sido removido.

    # Enlazamos las rutas de nuestras aplicaciones personalizadas
    path('', include('core.urls')),
    path('auth/', include('authentication.urls')),
    path('contratos/', include('contracts.urls')),
]