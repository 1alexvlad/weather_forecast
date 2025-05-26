from django.shortcuts import render

from rest_framework import viewsets

from weather.models import City
from .serializers import CitySerializer
from api.serializers import CitySerializer



class CityApiView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        city = self.get_object()
        city.count += 1
        city.save()
        serializer = self.get_serializer(city)
        return Response(serializer.data)
