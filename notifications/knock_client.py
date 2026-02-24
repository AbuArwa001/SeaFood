import os
from knockapi import Knock

# Use environment variable or fallback to string config if unavailable
KNOCK_API_KEY = os.getenv("KNOCK_SECRET_API_KEY", "sk_test_placeholder")

client = Knock(api_key=KNOCK_API_KEY)

def trigger_notification(workflow_key: str, recipients: list, data: dict = None):
    """
    Trigger a Knock workflow.
    recipients: a list of user IDs or dictionaries with id and email.
    data: Optional dictionary of variables for the template.
    """
    if data is None:
        data = {}
    
    try:
        response = client.workflows.trigger(
            key=workflow_key,
            recipients=recipients,
            data=data
        )
        return response
    except Exception as e:
        print(f"Error triggering knock workflow: {e}")
        return None
