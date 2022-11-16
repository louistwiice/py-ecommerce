import structlog

from celery import shared_task
from config.celery import app
from utilities.common import mail

logger = structlog.get_logger('app-logger')


@shared_task
def task_mail_user(subject: str, to: list, message: str):
    logger.info('SEND_MAIL_TO', to=to, subject=subject, message=message)
    mail(subject, to, message)
