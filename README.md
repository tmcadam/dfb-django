# DFB (Django)

## Prerequisites

`sudo apt install libpq-dev` (needed to install psycopg2)


## Environment Variables

Run this is in the shell to set environment variables from .env

`export $(egrep -v '^#' .env | xargs)`

Dotenv needs the following variables

  - ENVIRONMENT [development, staging, production]
  - DB_NAME
  - DB_HOST
  - DB_PORT
  - DB_USER
  - DB_PASS


## Database Settings

Create a database for the project, create a role and modify with the following. 

```CREATE ROLE some_user with PASSWORD 'very-strong-password' LOGIN;
ALTER ROLE some_user SET client_encoding TO 'utf8';
ALTER ROLE some_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE some_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE some_database TO some_user;
```

For running tests need
`ALTER ROLE some_user NOSUPERUSER CREATEDB NOCREATEROLE NOINHERIT LOGIN;`