import os

import requests
from django.core.management import BaseCommand
from django_celery_beat.models import PeriodicTask


class Command(BaseCommand):

    def handle(self, *args, **options):
        import json
        # from datetime import datetime, timedelta
        #
        # from django_celery_beat.models import PeriodicTask, \
        #     IntervalSchedule
        #
        # # Создаем интервал для повтора
        # schedule, created = IntervalSchedule.objects.get_or_create(
        #     every=10,
        #     period=IntervalSchedule.SECONDS,
        # )
        #
        # # Создаем задачу для повторения
        # PeriodicTask.objects.create(
        #     interval=schedule,
        #     name='1234',
        #     task='habits.tasks.debug_task',
        #     kwargs=json.dumps({
        #         'be_careful': True,
        #     }),
        #     expires=datetime.utcnow() + timedelta(hours=120)
        # )
        obj = PeriodicTask.objects.all().get(pk=14)
        print(obj.kwargs)