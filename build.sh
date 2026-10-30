#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Collect static files (CSS, icons, manifest)
python manage.py collectstatic --no-input

# Create Superuser if it doesn't exist
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); u, created = User.objects.get_or_create(username='Iniobong'); u.set_password('AlphaAdmin2026!'); u.save()"