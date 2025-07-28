import requests

API_KEY = "4dc756b5fe1e462983972458252807" 

def get_weather_data(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
        response = requests.get(url)
        if response.status_code == 200:
            res = response.json()
            return {
                "city": res["location"]["name"],
                "country": res["location"]["country"],
                "temp": res["current"]["temp_c"],
                "condition": res["current"]["condition"]["text"],
                "icon": res["current"]["condition"]["icon"],
                "humidity": res["current"]["humidity"],
                "wind_kph": res["current"]["wind_kph"]
            }
        else:
            return None
    except:
        return None
