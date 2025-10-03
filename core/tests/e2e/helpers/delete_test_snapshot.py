from core.tests.e2e.helpers.request import request


def delete_test_snapshot(snapshot_id):
    status, response_data = request(
        method="DELETE",
        endpoint=f"/api/snapshots/{snapshot_id}/delete/",
    )

    return status == 200


def delete_test_snapshots_by_event(event):
    status, response_data = request(
        method="GET",
        endpoint="/api/snapshots/search/",
    )

    if status == 200:
        snapshots = response_data.get("data", [])

        for snapshot in snapshots:
            if snapshot.get("event") == event:
                delete_test_snapshot(snapshot["id"])
