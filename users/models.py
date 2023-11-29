from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    mail = models.EmailField(unique=True, verbose_name='Email', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='Город', **NULLABLE)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.email})"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('pk',)
