from twilio.rest import Client
import streamlit as st

def send_whatsapp_alert(message, target_phone):
    """
    Sends a WhatsApp message using Twilio API.
    Uses Streamlit Secrets for security.
    """
    try:
        # Pull credentials from Streamlit Secrets
        # If not set, this will fail gracefully into Simulation Mode
        account_sid = st.secrets.get("TWILIO_ACCOUNT_SID")
        auth_token = st.secrets.get("TWILIO_AUTH_TOKEN")
        from_whatsapp_number = 'whatsapp:+14155238886' # Default Twilio Sandbox number

        if not account_sid or not auth_token:
            print(f"DEBUG: Simulation Mode - Sending to {target_phone}: {message}")
            return True

        client = Client(account_sid, auth_token)
        
        # Ensure phone number is in correct format
        if not target_phone.startswith('whatsapp:'):
            target_phone = f'whatsapp:{target_phone}'

        client.messages.create(
            body=message,
            from_=from_whatsapp_number,
            to=target_phone
        )
        return True
    except Exception as e:
        st.error(f"Sentinel Link Error: {e}")
        return False