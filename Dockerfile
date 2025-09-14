FROM python:3.13-bookworm

EXPOSE 8000

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install PostgreSQL 17 client
RUN apt-get update \
    && apt-get install -y wget gnupg lsb-release \
    && sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update \
    && apt-get install -y postgresql-client-17

# install Python dependencies
ADD ./requirements-locked.txt  .
RUN pip install --upgrade pip
RUN pip install -r requirements-locked.txt

# Copy app folders
ADD ./authors               ./authors
ADD ./biographies           ./biographies
ADD ./comments              ./comments
ADD ./common                ./common
ADD ./dfb                   ./dfb
ADD ./images                ./images
ADD ./pages                 ./pages
ADD ./scripts               ./scripts
ADD ./manage.py             ./manage.py
ADD ./gunicorn_config.py    ./gunicorn_config.py

RUN chmod +x ./scripts/wait-for-it.sh

# Clean up apt cache
RUN rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

# Run the Django application at container start
# Summernote has a missing migration
CMD ./scripts/wait-for-it.sh rabbitmq:5672 -t 30 \
    && python manage.py collectstatic --noinput --clear \
    && python manage.py makemigrations django_summernote \
    && python manage.py migrate \
    && gunicorn -c gunicorn_config.py dfb.wsgi:application
