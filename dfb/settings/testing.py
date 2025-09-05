# ruff : noqa: F405
import os
import dj_database_url
from .base import *  # noqa

ENVIRONMENT = "testing"
DEBUG = True
ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://127.0.0.1"]
SECRET_KEY = "django-insecure-69k-#kmlre&rb4uhf2*d5foi+1ee)wsck_%9z*--wbit3_dk9e"

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DJANGO_DB_URL", "sqlite:///db-test.sqlite3"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# Other email settings are in per-test settings overrides
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
