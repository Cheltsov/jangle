from django.contrib import admin
from .models import Client, ClientStock, LogsAction


# Register your models here.
class ClientAdminInline(admin.TabularInline):
    model = ClientStock


class ClassAdmin(admin.ModelAdmin):
    inlines = (ClientAdminInline,)


admin.site.register(Client, ClassAdmin)
admin.site.register(LogsAction)
