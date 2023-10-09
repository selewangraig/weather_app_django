from django.shortcuts import render
from decouple import config
import requests

# Create your views here.
def get_weather(city):
    api_key = config("API_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    params = {
        "q" : city,
        "appid" : api_key,
        "units" : "metric"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() #an exception for bad HTTP status codes
        data = response.json()
    except requests.exceptions.RequestException as e:
        #Handle network errors
        print("Network error:", e)
        data = None
    except ValueError as e:
        #Handle invalid JSON responses
        print("Invalid JSON response:", e)
        data = None
        
    return data

def index(request):
    city = None
    weather_data = None

    if request.method == "POST":
        city = request.POST.get("city")
        if city:
            weather_data = get_weather(city)
    
    return render(request, "weather_app/index.html", {"city": city, "weather_data": weather_data})