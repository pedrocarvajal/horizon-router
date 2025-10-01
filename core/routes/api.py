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
from core.controllers.deal import (
    create_deal,
    search_deals,
    update_deal,
    delete_deal,
)
from core.controllers.snapshot import (
    create_snapshot,
    search_snapshots,
    update_snapshot,
    delete_snapshot,
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
    path("deals/", create_deal, name="create_deal"),
    path("deals/search/", search_deals, name="search_deals"),
    path("deals/<int:deal_id>/", update_deal, name="update_deal"),
    path("deals/<int:deal_id>/delete/", delete_deal, name="delete_deal"),
    path("snapshots/", create_snapshot, name="create_snapshot"),
    path("snapshots/search/", search_snapshots, name="search_snapshots"),
    path("snapshots/<int:snapshot_id>/", update_snapshot, name="update_snapshot"),
    path(
        "snapshots/<int:snapshot_id>/delete/", delete_snapshot, name="delete_snapshot"
    ),
]
