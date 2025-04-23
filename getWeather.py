import requests
import geopy
from geopy.geocoders import Nominatim

WEATHER_API_KEY = "a7e8d457345fcc17553871458cb62c8d"
geolocator = Nominatim(user_agent="geoapi")
weather_info = None

def get_weather(city):
    location = geolocator.geocode(city)
    print("Latitude:", location.latitude)
    print("Longitude:", location.longitude)
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&units=metric&appid={WEATHER_API_KEY}"
    res = requests.get(url)
    data = res.json()
    weather_info = {
        'weather': data['weather'][0]['description'],
        'temp_info': {
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'min_temp': data['main']['temp_min'],
            'max_temp': data['main']['temp_max'],
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'sea_level': data['main']['sea_level']
        },
        'wind': {
            'speed': data['wind']['speed'],
            'degree': data['wind']['deg'],
            'gust': data['wind']['gust'],
        },
        'sys': {
            'sunrise': data['sys']['sunrise'],
            'sunset': data['sys']['sunset'],
        },
        'timezone': data['timezone'],
        'name': data['name'], 
    }
    print(weather_info)
    return weather_info



