from django.urls import path
from . import views

app_name = 'contracts'

urlpatterns = [
    # Listar contratos (la que conecta con tu botón del menú lateral)
    path('lista/', views.lista_contratos, name='lista'),
    
    # Ruta para registrar un nuevo contrato
    path('crear/', views.crear_contrato, name='crear'),
    
    # Ruta para ver los detalles de un contrato individual
    path('contratos/<int:pk>/', views.detalle_contrato, name='detalle_contrato'),
    
    # Ruta para editar un contrato existente
    path('contratos/<int:pk>/editar/', views.editar_contrato, name='editar_contrato'),
]