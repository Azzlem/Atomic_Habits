from django.db import models
from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Habits(models.Model):
    title = models.CharField(max_length=50, verbose_name='название привычки', **NULLABLE)
    description = models.TextField(verbose_name='описание привычки', **NULLABLE)
    place = models.CharField(max_length=50, verbose_name='место', **NULLABLE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='создатель')

    def __str__(self):
        return f'Привычка "{self.title}"'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ('title',)
