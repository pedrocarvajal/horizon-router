from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def sample_task(message):
    logger.info(f"Processing task with message: {message}")
    return f"Task completed: {message}"
