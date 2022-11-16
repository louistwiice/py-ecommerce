import os
import logging

import structlog
from celery import Celery, shared_task
from celery.signals import setup_logging

from django.conf import settings
from django_structlog.celery.steps import DjangoStructLogInitStep

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery("ecomgraphql")
app.steps['worker'].add(DjangoStructLogInitStep)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@setup_logging.connect
def receiver_setup_logging(loglevel, logfile, format, colorize, **kwargs):  # pragma: no cover
    logging.config.dictConfig(settings.LOGGING)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


@shared_task
def addition(x, y):
    return x + y
