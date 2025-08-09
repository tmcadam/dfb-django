#!/bin/bash

# Lives in the Django container, triggered by Github Action using SSH to remote server
# Needs to run before the application containers are started (they will just error)

# docker compose run -rm $APPLICATION_NAME bash /app/scripts/setup_db.sh

printf "Checking for Django database server being available\n"

DJANGO_DB_USER=$(echo $DJANGO_DB_URL | grep -oP "postgres://\K(.+?):" | cut -d: -f1)
DJANGO_DB_PASSWORD=$(echo $DJANGO_DB_URL | grep -oP "postgres://.*:\K(.+?)@" | cut -d@ -f1)
DJANGO_DB_HOST=$(echo $DJANGO_DB_URL | grep -oP "postgres://.*@\K(.+?):" | cut -d: -f1)
DJANGO_DB_PORT=$(echo $DJANGO_DB_URL | grep -oP "postgres://.*@.*:\K(\d+)/" | cut -d/ -f1)
DJANGO_DB_NAME=$(echo $DJANGO_DB_URL | grep -oP "postgres://.*@.*:.*/\K(.+?)$")

# Make sure the postgres container has started, it should come up as a depends-on if not already running
export PGPASSWORD=$POSTGRES_PASSWORD
until pg_isready -U $POSTGRES_USER -h $DJANGO_DB_HOST -p $DJANGO_DB_PORT -d $POSTGRES_DB ; do sleep 1 ; done


printf "Checking for Django database and user\n"
export PGPASSWORD=$DJANGO_DB_PASSWORD
psql -U $DJANGO_DB_USER -h $DJANGO_DB_HOST -p $DJANGO_DB_PORT $DJANGO_DB_NAME -c "SELECT version()" &> /dev/null;
retVal=$?
if [ $retVal -eq 0 ]; then
    printf "The Django database user already exists\n"
    exit 0
fi

printf "Initialising database, changing setting and user privileges\n"
export PGPASSWORD=$POSTGRES_PASSWORD
psql -U $POSTGRES_USER -h $DJANGO_DB_HOST -p $DJANGO_DB_PORT $POSTGRES_DB << EOF
CREATE DATABASE $DJANGO_DB_NAME;
CREATE USER $DJANGO_DB_USER WITH ENCRYPTED PASSWORD '$DJANGO_DB_PASSWORD';
GRANT ALL ON DATABASE $DJANGO_DB_NAME TO $DJANGO_DB_USER;
ALTER DATABASE $DJANGO_DB_NAME OWNER TO $DJANGO_DB_USER;
ALTER ROLE $DJANGO_DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DJANGO_DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DJANGO_DB_USER SET timezone TO 'UTC';
EOF

printf "Created Django database and user, modified user with correct settings and privileges\n"
