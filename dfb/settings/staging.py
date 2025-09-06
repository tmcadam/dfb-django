# ruff : noqa: F405
import os
import dj_database_url
from .base import *  # noqa

ENVIRONMENT = "staging"
DEBUG = False
ALLOWED_HOSTS = os.environ["DJANGO_ALLOWED_HOSTS"].split(",")
CSRF_TRUSTED_ORIGINS = os.environ["DJANGO_CSRF_TRUSTED_ORIGINS"].split(",")
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ["DJANGO_DB_URL"],
        conn_max_age=600,
        conn_health_checks=True,
    )
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.environ["DJANGO_EMAIL_HOST"]
EMAIL_PORT = os.environ["DJANGO_EMAIL_PORT"]
EMAIL_USE_SSL = os.environ["DJANGO_EMAIL_USE_SSL"]
EMAIL_HOST_USER = os.environ["DJANGO_EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["DJANGO_EMAIL_HOST_PASSWORD"]

COMMENT_EMAIL_RECIPIENTS = os.environ["DJANGO_COMMENT_EMAIL_RECIPIENTS"]
COMMENT_EMAIL_FROM = os.environ["DJANGO_COMMENT_EMAIL_FROM"]

# These will be removed when the queue and workers are fully configured
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
    },
}
