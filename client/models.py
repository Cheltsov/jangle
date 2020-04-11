from django.db import models

from jangle.constant import Country, ACTION
from stock.models import Stock


# Create your models here.


class Client(models.Model):
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    country = models.CharField(choices=Country, default='0', max_length=1)
    city = models.CharField(max_length=20)
    birthday = models.DateField()
    fio = models.CharField(max_length=50)
    money = models.FloatField(max_length=11, default=0)

    class Meta:
        ordering = ['fio']
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class ClientStock(models.Model):
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    id_stock = models.ForeignKey(Stock, on_delete=models.CASCADE)


class LogsAction(models.Model):
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    action = models.CharField(choices=ACTION, max_length=1)
    date_created = models.DateTimeField(auto_now_add=True)
    delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Действие клиента'
        verbose_name_plural = 'Действия клиента'
