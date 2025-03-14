#!/bin/bash

python /tmp/wait_for_postgres.py

set -e

echo "Applying database makemigrations..."
python portfolio/manage.py makemigrations

# flush database if DJANGO_FLUSH_DB is set to 1
if [ "$DJANGO_FLUSH_DB" = "1" ]; then
    echo "Flushing database..."
    python portfolio/manage.py flush --no-input
fi

echo "Applying database migrations..."
python portfolio/manage.py migrate

echo "Checking if superuser exists..."
python portfolio/manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        username='${DJANGO_SUPERUSER_USERNAME}',
        email='${DJANGO_SUPERUSER_EMAIL}',
        password='${DJANGO_SUPERUSER_PASSWORD}'
    )
    print('Superuser created.')
else:
    print('Superuser already exists. Skipping creation.')
"

exec "$@"