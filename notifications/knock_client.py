import os
from knockapi import Knock

# Use environment variable or fallback to string config if unavailable
KNOCK_API_KEY = os.getenv("KNOCK_SECRET_API_KEY", "sk_test_placeholder")

client = Knock(api_key=KNOCK_API_KEY)

def trigger_notification(workflow_key: str, recipients: list, data: dict = None, actor: str = None):
    """
    Trigger a Knock workflow.
    recipients: a list of user IDs or dictionaries with id and email.
    data: Optional dictionary of variables for the template.
    actor: Optional user ID representing the actor who performed the action.
    """
    if data is None:
        data = {}
    
    try:
        kwargs = {
            "key": workflow_key,
            "recipients": recipients,
            "data": data,
        }
        if actor:
            kwargs["actor"] = actor
            
        response = client.workflows.trigger(**kwargs)
        return response
    except Exception as e:
        print(f"Error triggering knock workflow: {e}")
        return None
