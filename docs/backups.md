# Backups

The system has a scheduled action `.github/workflows/backup.yml` that automatically backs up the uploaded image files and database contents and stores them in Onedrive.

## Backup Methodology

The backup runs using bash commands from the Github runner. The commands are running on the DFB server, but output is piped directly back to the Github action and stored in temporary files there, before pushing to Onedrive.

    - The first step is to create a tar of the `mediafiles` directory
    - Use the Django `dumpdata` command to create a json file of database contents
    - Use the pg_dump command to create a sql file of the database
    - Add both database files to tar archive and compress
    - If it is 1st day of month upload to `SWB_Backups\monthly`
    - Upload the same file to `SWB_Backups\daily`
    - House clean `SWB_Backups\daily` to remove backups older than 14days

Backups are currently aruond 500mb each. It is planned to maintain all monthly backups and keep 14days of daily backups.


## Backup Restoration

#### On the local machine.

Download backup from Onedrive and push to server.

    - `rclone copy onedrive:SWB_Backups/daily/dfb_backup_staging_20250914.tar.gz ./tmp`
    - `scp ./tmp/dfb_backup_staging_20250914.tar.gz <SSH_ALIAS>:infra/backup.tar.gz`

#### On the server.

Clear old data

    - `cd infra`
    - `docker compose exec dfb-django rm -rf mediafiles/*`
    - `docker compose exec dfb-django python manage.py flush`

Load new data

    - `docker compose cp backup.tar.gz dfb-django:/app`
    - `docker compose exec dfb-django tar -xzf backup.tar.gz`
    - `docker compose exec dfb-django python manage.py loaddata database.json`
    - or
    - `docker compose exec dfb-django cat backup.sql | docker compose exec -T dfb-django python manage.py dbshell`

Reset sequences in database

    - `docker compose exec dfb-django python manage.py sqlsequencereset biographies authors comments pages images | docker compose exec -T dfb-django python manage.py dbshell`


It may be useful to have an action that automatically restores a specified backup (i.e. restoring staging database from production is useful)

