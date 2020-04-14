from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_quotes, name='list_quotes'),
    path('refresh_con/', views.refresh_con, name='refresh_con'),
    path('get_grafic/<int:id>', views.get_grafic, name='get_grafic'),
    path('get_company/<int:id>', views.get_company, name='get_company'),
    path('predictValue/', views.predictValue, name='predictValue')
]
