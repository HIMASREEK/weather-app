import requests
from django.shortcuts import render
from django.conf import settings

def index(request):
    data = {}
    if request.method == 'POST':
        city = request.POST['city']
        api_key = getattr(settings, "OPENWEATHER_API_KEY", None)  # from settings.py
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
        try:
            response = requests.get(url).json()
            if response.get("cod") != 200:
                data['error'] = response.get("message", "City not found.")
            else:
                data = {
                    "country_code": response['sys']['country'],
                    "coordinate": f"{response['coord']['lon']}, {response['coord']['lat']}",
                    "temp": f"{response['main']['temp']} °C",
                    "pressure": response['main']['pressure'],
                    "humidity": response['main']['humidity'],
                    "main": response['weather'][0]['main'],
                    "description": response['weather'][0]['description'],
                    "icon": response['weather'][0]['icon'],
                }
        except Exception as e:
            data['error'] = f"Error fetching data: {str(e)}"
    return render(request, "main/index.html", data)
