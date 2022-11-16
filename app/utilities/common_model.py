import structlog

from django.db import models

logger = structlog.get_logger('app-logger')


class TimestampBase(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
