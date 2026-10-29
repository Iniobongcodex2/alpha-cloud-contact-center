import os
from twilio.rest import Client
from django.conf import settings

def make_outbound_call(to_number, from_number=None):
    """
    Initiates a real phone call using Twilio.
    """
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    
    if not account_sid or not auth_token:
        return {"status": "error", "message": "Twilio credentials are missing."}

    client = Client(account_sid, auth_token)

    # For Trial accounts, we use your Verified Caller ID as the 'From' number.
    # If you buy a Twilio number later, you can pass that instead.
    trial_from_number = "+971588984315"
    
    # Use the passed number, or fall back to the trial verified number
    actual_from = from_number if from_number else trial_from_number

    try:
        # This is the URL Twilio will request when the call is answered.
        twiml_instructions = '<Response><Say voice="alice">Welcome to ALPHA Cloud Contact Center. Your outbound call is connected.</Say></Response>'
        
        call = client.calls.create(
            twiml=twiml_instructions,
            to=to_number,
            from_=actual_from
        )
        return {"status": "success", "call_sid": call.sid}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}