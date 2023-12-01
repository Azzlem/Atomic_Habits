import datetime

from django.db import models

from config import settings
from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Action(models.Model):
    name = models.CharField(max_length=200, verbose_name='действие', default='Разминка')
    description = models.TextField(verbose_name='описание привычки', **NULLABLE)

    def __str__(self):
        return f'Надо сделать "{self.name}"'

    class Meta:
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'
        ordering = ('name',)


class Place(models.Model):
    name = models.CharField(max_length=200, verbose_name='место', default='дом')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'
        ordering = ('name',)


class Habits(models.Model):
    title = models.CharField(max_length=50, verbose_name='название привычки', **NULLABLE)
    description = models.TextField(verbose_name='описание привычки', **NULLABLE)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='создатель')
    action = models.ForeignKey(Action, on_delete=models.PROTECT, **NULLABLE, verbose_name='действие')
    place = models.ForeignKey(Place, on_delete=models.PROTECT, **NULLABLE, verbose_name='место')

    datetime_start = models.DateTimeField(default=datetime.datetime.now(), verbose_name='время выполнения')
    is_pleasure = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    pleasure_habit = models.ForeignKey('self', on_delete=models.PROTECT, **NULLABLE, verbose_name='приятная привычка')
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name='периодичность в днях')
    reward = models.CharField(max_length=150, **NULLABLE, verbose_name='вознаграждение')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')
    execution_time = models.PositiveSmallIntegerField(default=1, verbose_name='время на выполнение в минутах')




    def __str__(self):
        return f'Привычка "{self.title}"'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ('title',)
