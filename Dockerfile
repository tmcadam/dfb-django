FROM python:3.13.0-bookworm

EXPOSE 8000

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Postgres client
RUN apt update
RUN apt install postgresql-common -y
RUN /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh -y
RUN apt update
RUN apt install postgresql-client-16 -y

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

# Clean up apt cache
RUN rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

# Run the Django application at container start
CMD python manage.py collectstatic --noinput --clear \
    && python manage.py migrate \
    && gunicorn -c gunicorn_config.py dfb.wsgi:application
