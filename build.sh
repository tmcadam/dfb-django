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
rm -rf ${BASE_DIR}/static/vendor/fontawesome/
wget https://use.fontawesome.com/releases/v6.6.0/fontawesome-free-6.6.0-web.zip -P ${BASE_DIR}/tmp
unzip -d ${BASE_DIR}/tmp ${BASE_DIR}/tmp/fontawesome-free-6.6.0-web.zip
mkdir -p ${BASE_DIR}/static/vendor/fontawesome/scss
mkdir -p ${BASE_DIR}/static/vendor/fontawesome/webfonts
cp -r ${BASE_DIR}/tmp/fontawesome-free-6.6.0-web/scss ${BASE_DIR}/static/vendor/fontawesome/scss
cp -r ${BASE_DIR}/tmp/fontawesome-free-6.6.0-web/webfonts ${BASE_DIR}/static/vendor/fontawesome/webfonts


# Install Fonts
mkdir -p ${BASE_DIR}/static/vendor/fonts
wget https://www.1001fonts.com/download/open-sans.zip  -P ${BASE_DIR}/tmp
unzip -o -d ${BASE_DIR}/static/vendor/fonts ${BASE_DIR}/tmp/open-sans.zip
wget https://www.1001fonts.com/download/roboto-slab.zip  -P ${BASE_DIR}/tmp
unzip -o -d ${BASE_DIR}/static/vendor/fonts ${BASE_DIR}/tmp/roboto-slab.zip

python manage.py collectstatic -l --noinput

