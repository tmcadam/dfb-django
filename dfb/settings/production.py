# ruff : noqa: F405
from .base import *  # noqa

ENVIRONMENT = "production"
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
