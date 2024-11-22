# DFB V2(Django)

## Local Development Prerequisites

### Secrets/Environment Variables

Two secrets files are required and can be placed in the `./secrets` directory of the project. in production these can located anywhre and the paths updated in the relevant docker-compose file. 

`postgres.env` (only needed for initial database creation script)

- `POSTGRES_PASSWORD=[anything]` 
- `POSTGRES_USER=postgres` (generally `postgres` or other superuser for a local installation)
- `POSTGRES_DATABASE=postgres` (generally `postgres` for local installation)

`dfb-django-local.env`

- `APP_DB_NAME=dfb_django`
- `APP_DB_USER=django_user`
- `APP_DB_PASSWORD=django_user_password`
- `APP_DB_HOST=localhost`
- `APP_DB_PORT=5432`
- `DJANGO_ENV=local` environment level for debug etc. 
- `ALLOWED_HOSTS=localhost` comma seperated list of ALLOWED_HOSTS
- `ADMIN_PASSWORD=some-password` initial user for the Django admin

Load as environment variables:

`export $(egrep -v '^#' ./secrets/postgres.env | xargs)`
`export $(egrep -v '^#' ./secrets/dfb-django-local.env | xargs)`

### Postgresql 16 Server and Client Libraries 

NB. Make sure the environment variables have been set before running.

```
sudo apt install postgresql-common -y
sudo apt update
sudo apt install postgresql-16
sudo -u  postgres psql -c "ALTER USER postgres WITH ENCRYPTED PASSWORD '$POSTGRES_PASSWORD';"
sudo service postgresql restart
```

`bash ./scripts/database_setup.sh`
or
`docker compose run --rm  --build dfb-staging-setup bash ./scripts/database_setup.sh`

### Virtual Envionment and Install Dependencies
```
sudo apt install libpq-dev
python3 -m venv venv
pip install -r requirements.txt
pip install -r requirements-dev.txt
```


## Running Tests

We need to grant the db user createdb permissions.

`sudo -u  postgres psql -c "ALTER ROLE $APP_DB_USER CREATEDB;"`

The tests are configured to use pytest (but look like unittest)

The Vscode test discovery and GUI tools are configured

Run tests:
`pytest` (runs the full suite)
`pytest biographies/tests/test_models.py`
`pytest -m biographies`


## Loading Historical Data

TODO


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
