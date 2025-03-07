import json
import redis

from .worker import celery_app, logger
from ..core.settings import settings

r = redis.Redis(host='localhost', port=6379, db=0)
print(r.ping())


@celery_app.task(
    bind=True,
    name="app.crawl_site_task",
    max_retries=settings.CELERY_RETRIES_TIME,
)
def crawl_site_task(self, url, sender_info, recipient_info):
    try:
        print(self.request.id)
        logger.info(f"Crawling URL: {url}")
        data = {
            'url': url,
            'sender_info': sender_info,
            'recipient_info': recipient_info
        }
        return url
    except Exception as e:
        logger.error("Err", exc_info=True)
