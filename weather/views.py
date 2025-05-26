import requests
from django.shortcuts import render

from .forms import CityForm
from .models import City

def index(request, city_name=None):
    secret_key = '388940ebc962625ebaf71eaeb2ad39fd'
    error_message = None
    all_cities = []

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.save(commit=False)
            new_city.name = new_city.name.lower()
            form.save()
            cities = [new_city]
    else:
        form = CityForm()

    if city_name:
        try:
            city_obj = City.objects.get(name__iexact=city_name)
            cities = [city_obj]
        except City.DoesNotExist:
            error_message = f"Город '{city_name}' не найден в базе"
            cities = []
    else:
        cities = City.objects.all().order_by('-id')[:5]

    for city in cities:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city.name}&units=metric&appid={secret_key}'
        res = requests.get(url).json()
        
        if res.get('cod') != 200:
            error_message = f"Город '{city.name}' не найден"
            continue
            
        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon']
        }
        all_cities.append(city_info)

    context = {
        'all_info': all_cities,
        'form': form,
        'error_message': error_message
    }

    return render(request, 'weather/index.html', context)