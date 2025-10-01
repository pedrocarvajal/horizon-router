.ONESHELL:

run-dev:
	bash scripts/cleanup_macos_files.sh
	docker compose down
	docker compose up --build

run-db-seed:
	docker compose exec horizon-router-app python manage.py seed

run-db-clean:
	docker compose exec horizon-router-app python manage.py clean

run-db-migration:
	docker compose exec horizon-router-app python manage.py migrate

run-db-refresh:
	make run-db-clean
	make run-db-migration
	make run-db-seed
	
test-e2e:
	docker compose exec horizon-router-app python manage.py test core.tests.e2e

test-integration:
	docker compose exec horizon-router-app python manage.py test core.tests.integration

test-unit:
	docker compose exec horizon-router-app python manage.py test core.tests.unit

# execute-celery-task-update_crypto_calendar_events:
# 	docker compose exec map-celery-beat celery -A config call update_crypto_calendar_events
