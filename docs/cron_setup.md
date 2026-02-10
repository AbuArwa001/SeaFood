# Daily Exchange Rate Synchronization Setup

To ensure that the currency exchange rates are updated every day, you should set up a cron job on your server.

## Recommended Schedule
We recommend running the synchronization once a day, typically at midnight UTC or early in the morning.

## Cron Job Configuration

1.  Open your crontab editor:
    ```bash
    crontab -e
    ```

2.  Add the following line to the end of the file (adjust the paths to match your server environment):
    ```bash
    0 0 * * * cd /path/to/SeaFood && /path/to/SeaFood/.venv/bin/python3 manage.py sync_rates >> /path/to/SeaFood/logs/sync_rates.log 2>&1
    ```

    *   `0 0 * * *`: Runs at 00:00 (Midnight) every day.
    *   `cd /path/to/SeaFood`: Navigates to the project directory.
    *   `/path/to/SeaFood/.venv/bin/python3`: Uses the virtual environment's Python interpreter.
    *   `manage.py sync_rates`: Executes the synchronization command.
    *   `>> ... 2>&1`: Logs output and errors to a file for monitoring.

## Manual Trigger
You can also run the command manually at any time to refresh the rates:
```bash
source .venv/bin/activate
python3 manage.py sync_rates
```
