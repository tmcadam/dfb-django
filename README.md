# DFB V2(Django)

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
GRANT CREATE ON SCHEMA public TO some_user;
```

For running tests need
`ALTER ROLE some_user NOSUPERUSER CREATEDB NOCREATEROLE NOINHERIT LOGIN;`

## CI/CD

### Initial Deployment

This should take you to the point of an empty site without content. 

  - One off step
  - The database is initalised with the correct user
  - Media folder is ready for use
  - Static content has been copied
  - Migrations applied 
  - Initial admin user created

### Data Loading

This may suit semi-manual running, it is DFB specific, rather than application 

  - One off step
  - Run through a series of steps to preload data and media
  - Create users

### Continious Deployment

This will be run on push/merge to develop (staging environment) or main (production) branches. 

  - Rebuild images, push to Dockerhub
  - Trigger a restart of the container, with a force pull
  - Collect static files
  - Run migrations
  
## TODO

  - Tag/Version images
  - Setup action for staging and production deployments
  - Pin versions in requirements
  - Github action for running tests
