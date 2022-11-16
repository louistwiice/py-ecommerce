import string
import structlog
import redis

import rstr
from django.conf import settings
from django.core.mail import send_mail

from config import env

logger = structlog.get_logger('app-logger')

def generate_token(size: int = 5):
    return rstr.rstr(string.digits, size)


def get_redis_connection(db: int = None):
    logger.info('DB_INFO', db=db, redis_default_db=env.REDIS_DEFAULT_DB)
    if db is None:
        return redis.Redis.from_url(settings.REDIS_URL + str(env.REDIS_DEFAULT_DB))

    return redis.Redis.from_url(settings.REDIS_URL + str(db))


def mail(subject: str, emails:list, message: str):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            fail_silently=True,
        )
    except Exception as e:
        logger.error('MAIL_EXCEPTION', error=str(e))
