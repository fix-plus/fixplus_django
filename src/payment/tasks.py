import json

import requests
from django.conf import settings
from celery import shared_task


@shared_task(bind=True)
def send_online_payment_sms(self, data: dict):
    try:
        url = f'https://api.kavenegar.com/v1/{settings.SMS_API_KEY}/verify/lookup.json'
        params = {
            'receptor': data['receptor'],
            'token20': data['customer_name'],
            'token': data['amount'],
            'token2': data['url_context'],
            'template': data['template']
        }

        # Send the request
        response = requests.get(url, params=params)
        print(response)

        # Check response status
        return response.status_code == 200

    except Exception as e:
        # Log the exception or handle it accordingly
        return False

