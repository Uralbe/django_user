import re
from django.core.exceptions import ValidationError
from django.conf import settings
import requests
# from user.models import pattern
pattern = r'^(998)\d{9}$'

def validate_phone_number(phone_number):
    if not re.match(pattern, phone_number):
        raise ValidationError('phone_number is not valid')


def get_formatted_phone_number(phone_number):
    phone_number = re.sub('\D', '', phone_number)
    if len(phone_number) == 9:
        phone_number = "998" + phone_number
    if len(phone_number) != 12:
        raise ValidationError('phone_number is not valid')
    return phone_number


def get_message_payload(phone_number, message="Testing? provide message"):

    payload = {
        'mobile_phone': phone_number,
        'message': message,
    }

    return payload


ESKIZ_AUTH_URL = "http://notify.eskiz.uz/api/auth/login"


def get_token():
    payload = {
        'email': settings.ESKIZ_EMAIL,
        'password': settings.ESKIZ_SECRET_KEY
    }
    try:
        token = requests.post(ESKIZ_AUTH_URL, headers={},
                              json=payload).json()['data']['token']
    except Exception as ex:
        raise ValueError("Eskiz is not working!")
    return token


def get_header():
    header = {
        'Authorization': 'Bearer {}'.format(get_token()),
        'Content-type': 'application/json'
    }
    return header


def send_code_to_phone(code, phone_number, message):
    """Function that send the code to the user's phone number,
    we can use it to reset the password or sign up verification.
    """
    msg = "{} {}".format(message, code)
    payload = get_message_payload(phone_number, message)
    headers = get_header()
    res = requests.post(settings.ESKIZ_SMS_SEND_URL,
                        json=payload, headers=headers)
    return res
