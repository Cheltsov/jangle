from django.db import models

from client.models import Client
from jangle.constant import ACTION

# Create your models here.
class Bot(models.Model):
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    action = models.CharField(choices=ACTION, default='0', max_length=1)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    min_price = models.FloatField()
    max_price = models.FloatField()

    class Meta:
        verbose_name = 'Робот'
        verbose_name_plural = 'Роботы'
