from django.conf import settings
from authy.api import AuthyApiClient

authy = AuthyApiClient(settings.AUTHY_API_KEY)


def send_sms_verify(country_code, phone_number):
    return authy.phones.verification_start(phone_number, country_code, via='sms')

def check_sms_verify(country_code, phone_number, verification_code):
    return authy.phones.verification_check(phone_number, country_code, verification_code)
