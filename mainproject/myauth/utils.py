  #authentication
from django.contrib.auth.tokens import PasswordResetTokenGenerator
#import six

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.
                text_type(user.is_active))
generate_token=TokenGenerator()  

# authentication
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )

generate_token = TokenGenerator()





# from twilio.rest import Client
# from django.conf import settings

# def send_whatsapp_message(to, body):
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     from_whatsapp = f"whatsapp:{settings.WHATSAPP_SENDER_NUMBER}"
#     to_whatsapp = f"whatsapp:{to}"
#     message = client.messages.create(
#         body=body,
#         from_=from_whatsapp,
#         to=to_whatsapp
#     )
#     return message.sid

