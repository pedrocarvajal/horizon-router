from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("api/", include("core.routes.api")),
]

if settings.DEBUG or settings.ENV_MODE == "development":
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
