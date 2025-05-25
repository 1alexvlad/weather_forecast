from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.index, name='home'),
    path('<str:city_name>/', views.index, name='city_weather'),

]
