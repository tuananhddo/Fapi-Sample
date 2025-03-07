import logging

from celery import Celery
from ..core.settings import settings
from kombu import Exchange, Queue

celery_app: Celery = Celery(
    'postman',
    broker=settings.broker_url,
    backend=settings.CELERY_RESULT_BACKEND,
)
celery_app.autodiscover_tasks(['src.celery_worker.tasks'], force=True)
dead_letter_queue_option = {
    "x-dead-letter-exchange": settings.CELERY_DLQ_EXCHANGE,
    "x-dead-letter-routing-key": settings.CELERY_DLQ_ROUTING_KEY,
}

default_exchange = Exchange(settings.CELERY_DEFAULT_EXCHANGE, type="direct")
dlx_exchange = Exchange(settings.CELERY_DLQ_EXCHANGE, type="direct")

default_queue = Queue(
    settings.CELERY_DEFAULT_QUEUE,
    default_exchange,
    routing_key=settings.CELERY_DEFAULT_ROUTING_KEY,
    queue_arguments=dead_letter_queue_option,
)

dead_letter_queue = Queue(
    settings.CELERY_DLQ_QUEUE, dlx_exchange, routing_key=settings.CELERY_DLQ_ROUTING_KEY
)

celery_app.conf.task_queues = (default_queue,)

celery_app.conf.task_default_queue = settings.CELERY_DEFAULT_QUEUE
celery_app.conf.task_default_exchange = settings.CELERY_DEFAULT_EXCHANGE
celery_app.conf.task_default_routing_key = settings.CELERY_DEFAULT_ROUTING_KEY

logger = logging.getLogger("__main__")

# app.conf.timezone = DateUtil.default_zone
# app.conf.update({
#     'task_queues':
#     [
#         Queue('delete_file'),
#         Queue('update_result_status')
#     ],
#     'task_routes': {
#         'delete_file': {'queue': 'delete_file'},
#         'update_result_status': {'queue': 'update_result_status'},
#     },
#     'beat_schedule': {
#         'add-every-30-seconds': {
#             'task': 'delete_file',
#             'schedule': 7200.0,
#             'args': (16, 16)
#         },
#         'update_result_status': {
#             'task': 'update_result_status',
#             'schedule': 1800.0
#         },
#     }
# })

if __name__ == "__main__":
    argv = [
        'worker',
        '--loglevel=INFO',
        '--pool=solo'  # Window opts
    ]
    celery_app.worker_main(argv)