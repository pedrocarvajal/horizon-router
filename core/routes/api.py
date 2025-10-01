from django.urls import path
from core.controllers.health import health
from core.controllers.heartbeat import create_heartbeat
from core.controllers.account import (
    create_account,
    search_accounts,
    update_account,
    delete_account,
)

urlpatterns = [
    path("health/", health, name="health"),
    path("heartbeat/", create_heartbeat, name="create_heartbeat"),
    path("accounts/", create_account, name="create_account"),
    path("accounts/search/", search_accounts, name="search_accounts"),
    path("accounts/<int:account_id>/", update_account, name="update_account"),
    path("accounts/<int:account_id>/delete/", delete_account, name="delete_account"),
]
