from django.urls import path
from core.controllers.HealthController import health
from core.controllers.HeartbeatController import create_heartbeat

urlpatterns = [
    path("health/", health, name="health"),
    path("heartbeat/", create_heartbeat, name="create_heartbeat"),
]
