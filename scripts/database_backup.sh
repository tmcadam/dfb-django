#!/bin/bash

DJANGO_DB_USER=$(echo $DJANGO_DB_URL | grep -oP "postgres://\K(.+?):" | cut -d: -f1)
DJANGO_DB_PASSWORD=$(echo $DJANGO_DB_URL | grep -oP "postgres://.*:\K(.+?)@" | cut -d@ -f1)
DJANGO_DB_HOST=$(echo $DJANGO_DB_URL | grep -oP "postgres://.*@\K(.+?):" | cut -d: -f1)
DJANGO_DB_PORT=$(echo $DJANGO_DB_URL | grep -oP "postgres://.*@.*:\K(\d+)/" | cut -d/ -f1)
DJANGO_DB_NAME=$(echo $DJANGO_DB_URL | grep -oP "postgres://.*@.*:.*/\K(.+?)$")

export PGPASSWORD=$DJANGO_DB_PASSWORD
pg_dump --clean -U $DJANGO_DB_USER -h $DJANGO_DB_HOST -p $DJANGO_DB_PORT -d $DJANGO_DB_NAME
