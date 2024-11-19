#!/bin/bash

# Lives in the Django container, triggered by Github Action using SSH to remote server
# Needs to run before the application containers are started (they will just error) 

# docker compose run -rm $APPLICATION_NAME bash /app/scripts/setup_db.sh

printf "Checking for Django database server being available\n"

# Make sure the postgres container has started, it should come up as a depends-on if not already running
export PGPASSWORD=$POSTGRES_PASSWORD 
until pg_isready -U $POSTGRES_USER -h $APP_DB_HOST -p $APP_DB_PORT -d $POSTGRES_DB ; do sleep 1 ; done


printf "Checking for Django database and user\n"
export PGPASSWORD=$APP_DB_PASSWORD 
psql -U $APP_DB_USER -h $APP_DB_HOST -p $APP_DB_PORT $APP_DB_NAME -c "SELECT version()" &> /dev/null;
retVal=$?
if [ $retVal -eq 0 ]; then 
    printf "The Django database user already exists\n"
    exit 0
fi

printf "Initialising database, changing setting and user privileges\n"
export PGPASSWORD=$POSTGRES_PASSWORD 
psql -U $POSTGRES_USER -h $APP_DB_HOST -p $APP_DB_PORT $POSTGRES_DB << EOF
CREATE DATABASE $APP_DB_NAME;
CREATE USER $APP_DB_USER WITH ENCRYPTED PASSWORD '$APP_DB_PASSWORD';
GRANT ALL ON DATABASE $APP_DB_NAME TO $APP_DB_USER;
ALTER DATABASE $APP_DB_NAME OWNER TO $APP_DB_USER;
ALTER ROLE $APP_DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $APP_DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $APP_DB_USER SET timezone TO 'UTC';
EOF

printf "Created Django database and user, modified user with correct settings and privileges\n"
