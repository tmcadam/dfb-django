#!/bin/bash

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

mkdir -p ${BASE_DIR}/tmp
mkdir -p ${BASE_DIR}/static/vendor

# Install bootstrap to static folder
wget https://github.com/twbs/bootstrap/archive/v4.1.3.zip -P ${BASE_DIR}/tmp
unzip -d ${BASE_DIR}/tmp ${BASE_DIR}/tmp/v4.1.3.zip
mkdir -p ${BASE_DIR}/static/vendor/bootstrap
cp -r ${BASE_DIR}/tmp/bootstrap-4.1.3/scss/* ${BASE_DIR}/static/vendor/bootstrap

# Install fontawesome to static folder
wget https://fontawesome.com/v4.7/assets/font-awesome-4.7.0.zip -P ${BASE_DIR}/tmp
unzip -d ${BASE_DIR}/tmp ${BASE_DIR}/tmp/font-awesome-4.7.0.zip
mkdir -p ${BASE_DIR}/static/vendor/fontawesome
cp -r ${BASE_DIR}/tmp/font-awesome-4.7.0/scss/* ${BASE_DIR}/static/vendor/fontawesome


# Install Fonts
mkdir -p ${BASE_DIR}/static/vendor/fonts
wget https://www.1001fonts.com/download/open-sans.zip  -P ${BASE_DIR}/tmp
unzip -o -d ${BASE_DIR}/static/vendor/fonts ${BASE_DIR}/tmp/open-sans.zip
wget https://www.1001fonts.com/download/roboto-slab.zip  -P ${BASE_DIR}/tmp
unzip -o -d ${BASE_DIR}/static/vendor/fonts ${BASE_DIR}/tmp/roboto-slab.zip

python manage.py collectstatic -l --noinput

