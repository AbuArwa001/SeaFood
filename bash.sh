#!/usr/bin/env bash
VIRTUAL_ENV_DIR="./venv"

# Create virtual environment if it doesn't exist
if [ ! -d "$VIRTUAL_ENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VIRTUAL_ENV_DIR"
fi

# Activate the virtual environment
if [ -z "$VIRTUAL_ENV_DIR" ]; then
    echo "Activating virtual environment..."
    source ./venv/bin/activate
fi

# Install any new dependencies
pip install -r requirements.txt

python manage.py makemigrations
# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
