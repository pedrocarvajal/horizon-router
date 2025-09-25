from django.urls import path
from core.controllers.health import health
from core.controllers.heartbeat import create_heartbeat

urlpatterns = [
    path("health/", health, name="health"),
    path("heartbeat/", create_heartbeat, name="create_heartbeat"),
]
