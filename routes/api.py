from django.urls import path
from controllers.HealthController import health

urlpatterns = [
    path("health/", health, name="health"),
]
