#!/usr/bin/env bash
# Render build script — run as the "Build Command" in the Render dashboard.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
