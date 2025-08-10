#!/bin/bash

admin=$(python manage.py shell <<EOF
from django.contrib.auth.models import User
print (User.objects.filter(username="admin").count())
EOF
)

if [ $admin -eq 0 ]; then
printf "Creating admin user\n"
export DJANGO_SUPERUSER_PASSWORD=$DJANGO_ADMIN_PASSWORD
python manage.py createsuperuser --username admin --email admin@admin.com --no-input
else
printf "Updating admin password\n"
python manage.py shell <<EOF
from django.contrib.auth.models import User
u = User.objects.get(username="admin")
u.set_password("$DJANGO_ADMIN_PASSWORD")
u.save()
EOF
fi
