from django.urls import path
from . import views

app_name = 'contracts'

urlpatterns = [
    # -------------------------
    # Terceros
    # -------------------------
    path(
        "terceros/",
        views.lista_terceros,
        name="lista_terceros"
    ),
    path(
        "terceros/crear/",
        views.crear_tercero,
        name="crear_tercero"
    ),
    path(
        "terceros/<int:pk>/json/",  # <-- Cambio aplicado aquí
        views.obtener_tercero,
        name="obtener_tercero"
    ),
    path(
        "terceros/<int:pk>/editar/",
        views.editar_tercero,
        name="editar_tercero"
    ),

    # -------------------------
    # Áreas
    # -------------------------
    path(
        "areas/",
        views.lista_areas,
        name="lista_areas"
    ),
    path(
        "areas/crear/",
        views.crear_area,
        name="crear_area"
    ),
    path(
        "areas/<int:pk>/editar/",
        views.editar_area,
        name="editar_area"
    ),

    # -------------------------
    # Empresas
    # -------------------------
    path(
        "empresas/",
        views.lista_empresas,
        name="lista_empresas"
    ),
    path(
        "empresas/crear/",
        views.crear_empresa,
        name="crear_empresa"
    ),
    path(
        "empresas/<int:pk>/editar/",
        views.editar_empresa,
        name="editar_empresa"
    ),

    # -------------------------
    # Supervisores
    # -------------------------
    path(
        "supervisores/",
        views.lista_supervisores,
        name="lista_supervisores"
    ),
    path(
        "supervisores/crear/",
        views.crear_supervisor,
        name="crear_supervisor"
    ),
    path(
        "supervisores/<int:pk>/editar/",
        views.editar_supervisor,
        name="editar_supervisor"
    ),
    # NUEVA RUTA: Obtener JSON del supervisor
    path(
        "supervisores/<int:pk>/json/",
        views.obtener_supervisor,
        name="obtener_supervisor"
    ),

    # -------------------------
    # Contratos
    # -------------------------
    # Listar contratos (la que conecta con tu botón del menú lateral)
    path('lista/', views.lista_contratos, name='lista'),
    
    # Ruta para registrar un nuevo contrato
    path('crear/', views.crear_contrato, name='crear'),
    
    # Ruta para ver los detalles de un contrato individual
    path('contratos/<int:pk>/', views.detalle_contrato, name='detalle_contrato'),
    
    # Ruta para editar un contrato existente
    path('contratos/<int:pk>/editar/', views.editar_contrato, name='editar_contrato'),

    # Ruta para subir documentos al contrato
    path(
        "contratos/<int:pk>/documentos/",
        views.subir_documento,
        name="subir_documento"
    ),
]