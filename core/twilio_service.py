import os
from twilio.rest import Client
from django.conf import settings

def make_outbound_call(to_number, from_number):
    """
    Initiates a real phone call using Twilio.
    """
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    
    if not account_sid or not auth_token:
        return {"status": "error", "message": "Twilio credentials are missing."}

    client = Client(account_sid, auth_token)

    try:
        # This is the URL Twilio will request when the call is answered.
        # For now, it will just play a message so we can test the connection.
        twiml_instructions = '<Response><Say voice="alice">Welcome to ALPHA Cloud Contact Center. Your outbound call is connected.</Say></Response>'
        
        call = client.calls.create(
            twiml=twiml_instructions,
            to=to_number,
            from_=from_number
        )
        return {"status": "success", "call_sid": call.sid}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}