from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth_index, name='auth_index'),
    path('auth_main/', views.auth_main, name='auth_main'),
    path('registration/', views.registration, name='registration'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('logout/', views.logout, name='logout'),
]
