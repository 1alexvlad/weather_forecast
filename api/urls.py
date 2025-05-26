from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CityApiView
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'api/city', CityApiView, basename='city')


urlpatterns = [
    
]

urlpatterns += router.urls
