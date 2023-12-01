import os

import requests
from django.conf import settings


# def send_tg(*args, **kwargs):
#     token = settings.BOT_TOKEN
#     chat_id = settings.CHAT_ID
#
#     params = {
#         'chat_id': chat_id,
#         'text': f"Я буду {kwargs['action']} в {kwargs['place']} в {kwargs['place']}"
#     }
#     url = f"https://api.telegram.org/bot{token}/sendMessage"
#     response = requests.get(url, params=params)
#     response.raise_for_status()
#     return response.json()
#

def make_task(new_habit):
    import json
    from datetime import datetime, timedelta

    from django_celery_beat.models import PeriodicTask, \
        IntervalSchedule

    # Создаем интервал для повтора
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )

    # Создаем задачу для повторения
    PeriodicTask.objects.create(
        interval=schedule,
        name=f'{new_habit.pk}',
        task='habits.tasks.debug_task',
        kwargs=json.dumps({
            'action': new_habit.action.name,
            'place': new_habit.place.name,
            'time': new_habit.execution_time,
            'reward': new_habit.reward,
        }),
        expires=datetime.now() + timedelta(days=365),
        start_time=str(new_habit.datetime_start),
    )


def delete_task(habit_pk):
    """ Удаляет периодическую задачу. """

    import json
    from datetime import datetime, timedelta

    from django_celery_beat.models import PeriodicTask, \
        IntervalSchedule

    if PeriodicTask.objects.filter(name=str(habit_pk)).exists():
        periodic_task = PeriodicTask.objects.get(name=str(habit_pk))
        periodic_task.delete()
