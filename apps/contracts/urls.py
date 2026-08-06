from django.urls import path
from . import views
from .views.plantillas_documentales import *  # <-- Import de plantillas

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
        "terceros/<int:pk>/json/",
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
    path(
        "supervisores/<int:pk>/json/",
        views.obtener_supervisor,
        name="obtener_supervisor"
    ),

    # -------------------------
    # Tipos de Contrato
    # -------------------------
    path(
        "tipos-contrato/",
        views.lista_tipos_contrato,
        name="lista_tipos_contrato"
    ),
    path(
        "tipos-contrato/crear/",
        views.crear_tipo_contrato,
        name="crear_tipo_contrato"
    ),
    path(
        "tipos-contrato/<int:pk>/editar/",
        views.editar_tipo_contrato,
        name="editar_tipo_contrato"
    ),

    # -------------------------
    # Tipos de Documento Contractual
    # -------------------------
    path(
        "tipos-documento/",
        views.lista_tipos_documento,
        name="lista_tipos_documento",
    ),
    path(
        "tipos-documento/crear/",
        views.crear_tipo_documento,
        name="crear_tipo_documento",
    ),
    path(
        "tipos-documento/<int:pk>/editar/",
        views.editar_tipo_documento,
        name="editar_tipo_documento",
    ),

    # -------------------------
    # Contratos
    # -------------------------
    path('lista/', views.lista_contratos, name='lista'),
    path('crear/', views.crear_contrato, name='crear'),
    path('contratos/<int:pk>/', views.detalle_contrato, name='detalle_contrato'),
    path('contratos/<int:pk>/editar/', views.editar_contrato, name='editar_contrato'),
    path(
        "contratos/<int:pk>/documentos/",
        views.subir_documento,
        name="subir_documento"
    ),

    # -------------------------
    # Plantillas Documentales
    # -------------------------
    path(
        "plantillas/",
        lista_plantillas,
        name="lista_plantillas",
    ),
    path(
        "plantillas/<int:tipo_id>/",
        detalle_plantilla,
        name="detalle_plantilla",
    ),
]