from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER

class SMSClient:
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        self.from_number = TWILIO_FROM_NUMBER

    def send_sms(self, to_number: str, message: str):
        if not to_number:
            raise ValueError("Missing recipient phone number")
        msg = self.client.messages.create(body=message, from_=self.from_number, to=to_number)
        return {"sid": msg.sid, "status": msg.status}
