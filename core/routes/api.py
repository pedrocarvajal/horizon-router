from django.urls import path
from core.controllers.health import health
from core.controllers.heartbeat import create_heartbeat
from core.controllers.account import (
    create_account,
    search_accounts,
    update_account,
    delete_account,
)
from core.controllers.strategy import (
    create_strategy,
    search_strategies,
    update_strategy,
    delete_strategy,
)

urlpatterns = [
    path("health/", health, name="health"),
    path("heartbeat/", create_heartbeat, name="create_heartbeat"),
    path("accounts/", create_account, name="create_account"),
    path("accounts/search/", search_accounts, name="search_accounts"),
    path("accounts/<int:account_id>/", update_account, name="update_account"),
    path("accounts/<int:account_id>/delete/", delete_account, name="delete_account"),
    path("strategies/", create_strategy, name="create_strategy"),
    path("strategies/search/", search_strategies, name="search_strategies"),
    path("strategies/<int:strategy_id>/", update_strategy, name="update_strategy"),
    path(
        "strategies/<int:strategy_id>/delete/", delete_strategy, name="delete_strategy"
    ),
]
