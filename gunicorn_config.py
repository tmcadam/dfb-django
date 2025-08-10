"""gunicorn WSGI server configuration."""

from os import environ

bind = "0.0.0.0:" + environ.get("DJANGO_PORT", "8000")
capture_output = True
enable_stdio_inheritance = True
errorlog = "-"
accesslog = "-"
