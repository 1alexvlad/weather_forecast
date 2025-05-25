import requests

from django.shortcuts import render

from .models import City
from .forms import CityForm


def index(request):
    secret_key = '388940ebc962625ebaf71eaeb2ad39fd'

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all().order_by('-id')[:5]


    all_cities = []
    
    for city in cities:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={secret_key}'
        res = requests.get(url).json()

        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon']
        }

        all_cities.append(city_info)

    context = {
        'all_info': all_cities,
        'form': form
    }

    return render(request, 'weather/index.html', context)