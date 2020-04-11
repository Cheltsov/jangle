from django.db import models

# Create your models here.
class Stock(models.Model):
    company = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['company']
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

class StockPrice(models.Model):
    id_stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    open = models.DecimalField(max_length=20, decimal_places=7, max_digits=10000, default=0)
    high = models.DecimalField(max_length=20, decimal_places=7, max_digits=10000, default=0)
    low = models.DecimalField(max_length=20, decimal_places=7, max_digits=10000, default=0)
    close = models.DecimalField(max_length=20, decimal_places=7, max_digits=10000, default=0)
    vol = models.IntegerField(default=0)
