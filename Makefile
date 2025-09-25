.ONESHELL:

run-dev:
	bash scripts/cleanup_macos_files.sh
	docker compose down
	docker compose up --build

run-seed:
	docker compose exec horizon-router-app python manage.py seed

run-migration:
	docker compose exec horizon-router-app python manage.py migrate
	
# test: 
# 	docker compose exec horizon-router-app python manage.py test core

# execute-celery-task-update_crypto_calendar_events:
# 	docker compose exec map-celery-beat celery -A config call update_crypto_calendar_events
