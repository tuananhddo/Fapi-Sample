from .worker import celery_app, logger
from ..core.settings import settings

@celery_app.task(
    bind=True,
    name="app.data_collection_task",
    max_retries=settings.CELERY_RETRIES_TIME,
)
def data_collection_task(self, url, x, y):
    try:
        print(self.request.id)
        logger.info(f"Crawling URL: {url}")
        return url
    except Exception as e:
        logger.error("Err", exc_info=True)
