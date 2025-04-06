import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import re
from dotenv import load_dotenv
load_dotenv()

class WhatsAppAlert:
    def __init__(self):
        # Load credentials from environment variables
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID', 'YOUR_TWILIO_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN', 'YOUR_TWILIO_TOKEN')
        self.client = Client(self.account_sid, self.auth_token)
        self.twilio_number = 'whatsapp:+14155238886'  # Twilio's WhatsApp sandbox number

    def _validate_number(self, number):
        """Validate Indian mobile number format"""
        return bool(re.match(r'^[6-9]\d{9}$', str(number)))

    def send(self, message, farmer_number):
        """
        Send WhatsApp message with error handling
        Args:
            message: str - Message content (max 1600 chars)
            farmer_number: str/int - Indian mobile number (10 digits without country code)
        Returns:
            dict: {'status': 'success/error', 'message_id': str, 'error': str}
        """
        try:
            # Input validation
            if not message or len(message) > 1600:
                raise ValueError("Message must be 1-1600 characters")
            
            if not self._validate_number(farmer_number):
                raise ValueError("Invalid Indian mobile number format")

            # Remove any prefixes/special characters
            clean_number = re.sub(r'[^0-9]', '', str(farmer_number))
            if len(clean_number) == 10:
                clean_number = f'91{clean_number}'  # Add India country code
            
            # Send message
            msg = self.client.messages.create(
                body=message[:1600],  # Ensure length limit
                from_=self.twilio_number,
                to=f'whatsapp:+{clean_number}'
            )
            
            return {
                'status': 'success',
                'message_id': msg.sid,
                'to': clean_number
            }
            
        except TwilioRestException as e:
            return {
                'status': 'error',
                'error': f"Twilio API error: {str(e)}",
                'code': e.code
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

# Usage example:
if __name__ == "__main__":
    alert = WhatsAppAlert()
    result = alert.send(
        "Your loan of ₹50,000 has been approved! Interest rate: 7.5%",
        "9876543210"  # Test number
    )
    print(result)