import requests
import streamlit as st

API_KEY = st.secrets["WEATHER_API_KEY"]

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
