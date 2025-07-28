import streamlit as st

def get_quote(condition):
    condition = condition.lower()
    if "rain" in condition:
        return "☔ Don't forget your umbrella!"
    elif "clear" in condition or "sun" in condition:
        return "😎 A great day to enjoy the sunshine!"
    elif "cloud" in condition:
        return "☁️ A cozy cloudy day. Maybe a chai break?"
    elif "mist" in condition or "fog" in condition:
        return "🌫️ Visibility is low — drive safe!"
    elif "wind" in condition:
        return "💨 Hold onto your dupatta — it's breezy!"
    elif "snow" in condition:
        return "❄️ Stay warm — winter wonderland outside!"
    else:
        return "🌍 Be prepared for anything — it's unpredictable!"

def get_sound_file(condition):
    condition = condition.lower()
    if "rain" in condition:
        return "assets/sounds/rain.mp3"
    elif "clear" in condition or "sun" in condition:
        return "assets/sounds/sunny.mp3"
    elif "wind" in condition or "breeze" in condition:
        return "assets/sounds/wind.mp3"
    else:
        return None

def apply_custom_css():
    with open("utils/styles.css") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)
