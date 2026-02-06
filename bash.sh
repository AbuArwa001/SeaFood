#!/usr/bin/env bash
VIRTUAL_ENV_DIR=".venv"

# Create virtual environment if it doesn't exist
# Exit immediately if a command exits with a non-zero status
set -o errexit

VIRTUAL_ENV_DIR=".venv"

# Create virtual environment if it doesn't exist
if [ ! -d "$VIRTUAL_ENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VIRTUAL_ENV_DIR"
fi

# Activate the virtual environment
if [ -f "$VIRTUAL_ENV_DIR/bin/activate" ]; then
    echo "Activating virtual environment..."
    source "$VIRTUAL_ENV_DIR/bin/activate"
fi

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py makemigrations
python manage.py migrate --run-syncdb

# Destructive commands disabled for production safety
python manage.py loaddata data.json
# python reset_passwords.py
# python manage.py seed_users

# Optional setup scripts (uncomment if needed)
# python manage.py seed_currencies
# python manage.py sync_rates
# python manage.py create_admin

# Collect static files
python manage.py collectstatic --noinput
