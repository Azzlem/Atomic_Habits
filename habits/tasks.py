import requests
from celery import shared_task
from config import settings


@shared_task()
def debug_task(**kwargs):
    token = settings.BOT_TOKEN
    chat_id = settings.CHAT_ID

    params = {
        'chat_id': chat_id,
        'text': f"Я буду {kwargs['action']} в течении {kwargs['time']} минуты в {kwargs['place']}"
    }
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
