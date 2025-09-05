# ruff : noqa: F405
import os
import dj_database_url
from .base import *  # noqa


ENVIRONMENT = "local"
DEBUG = True
ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://127.0.0.1"]
SECRET_KEY = "django-insecure-69k-#kmlre&rb4uhf2*d5foi+1ee)wsck_%9z*--wbit3_dk9e"

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DJANGO_DB_URL", "sqlite:///db.sqlite3"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "emails"  # change this to a proper location

CELERY_TASK_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES = True
