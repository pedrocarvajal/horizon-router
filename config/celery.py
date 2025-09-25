import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("horizon-router")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    # "sample-task": {
    #     "task": "services.SampleService.sample_task",
    #     "schedule": 60.0,
    #     "args": ("Hello from Celery Beat!",),
    # },
}
app.conf.timezone = "UTC"


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
