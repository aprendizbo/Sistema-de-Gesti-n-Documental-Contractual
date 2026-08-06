from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # El panel administrativo por defecto de Django ha sido removido.

    path('', include('core.urls')),
    path('auth/', include('authentication.urls')),
    path('contratos/', include('contracts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )