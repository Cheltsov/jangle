from django.contrib import admin
from .models import Stock, StockPrice


# Register your models here.
class StockAdminInline(admin.TabularInline):
    model = StockPrice


class ClassAdmin(admin.ModelAdmin):
    inlines = (StockAdminInline,)


admin.site.register(Stock, ClassAdmin)
