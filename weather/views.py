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
            city_name = form.cleaned_data['name'].lower()
            city, created = City.objects.get_or_create(name=city_name)
            if not created:
                city.count += 1
                city.save()

            history = request.session.get('history', [])
            if city_name not in history:
                history.insert(0, city_name) 
                history = history[:5]  
                request.session['history'] = history

            cities = City.objects.filter(name__in=history)
        else:
            cities = City.objects.all().order_by('-id')[:5]
    else:
        form = CityForm()
        if city_name:
            try:
                city_obj = City.objects.get(name__iexact=city_name.lower())
                cities = [city_obj]
            except City.DoesNotExist:
                error_message = f"Город '{city_name}' не найден в базе"
                cities = []
        else:
            history = request.session.get('history', [])
            if history:
                cities = City.objects.filter(name__in=history)
            else:
                cities = City.objects.all().order_by('-id')[:5]

    for city in cities:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city.name}&units=metric&appid={secret_key}'
        res = requests.get(url).json()

        if res.get('cod') != 200:
            error_message = f"Город '{city.name}' не найден в OpenWeather"
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
        'error_message': error_message,
        'city_name': city_name
    }

    return render(request, 'weather/index.html', context)
