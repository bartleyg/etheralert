from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.conf import settings
from twilio.rest import Client


# Uses credentials from the TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
# environment variables
client = Client()

@shared_task
def send_text(entry, tx):

    body = 'Address {0} got {1} ETH from {2} in Block {3} Tx {4}'.format(
        entry.address[0:6],
        tx['value'],
        tx['from'][0:6],
        tx['blockNumber'],
        tx['hash'][0:6]
    )

    message = client.messages.create(
        body=body,
        to=entry.phone_number,
        from_=settings.TWILIO_NUMBER,
    )