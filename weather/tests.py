import pytest
from django.urls import reverse
from weather.models import City
from django.db.utils import IntegrityError

@pytest.mark.django_db
def test_city_creation():
    """Тест создания города"""
    city = City.objects.create(name="London")
    assert city.name == "London"
    assert str(city) == "London"

@pytest.mark.django_db
def test_city_uniqueness():
    """Тест уникальности названия города"""
    City.objects.create(name="Каир")
    with pytest.raises(IntegrityError):
        City.objects.create(name="Каир")

@pytest.mark.django_db
def test_index_view_get(client):
    """Тест GET-запроса к главной странице"""
    response = client.get(reverse('weather:home'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_index_view_post(client):
    """Тест POST-запроса с добавлением города"""
    response = client.post(reverse('weather:home'), {'name': 'Berlin'})
    assert response.status_code == 200
    assert City.objects.filter(name='Berlin').exists()