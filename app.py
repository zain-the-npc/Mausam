import streamlit as st
import os
import random
from api.weather_api import get_weather_data # Assuming this exists and works
import streamlit.components.v1 as components
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="Mausam - Your Daily Forecast",
    layout="centered", # 'wide' can also be used depending on desired aesthetic
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "A cutting-edge weather app for the modern user. Designed by Gemini."
    }
)

# --- Inject Custom Fonts and CSS ---
# Now including Open Sans for the main title.
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600;700&family=Open+Sans:wght@700&family=Roboto+Mono&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Load custom CSS
# Ensure your styles.css is in a 'utils' folder relative to app.py
try:
    with open("utils/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error("`styles.css` not found! Please ensure it's in `utils/styles.css` relative to your `app.py`.")


# --- Audio Playback Function (Helper) ---
def play_background_sound(sound_path):
    """Embeds an autoplaying, looping audio file."""
    if not os.path.exists(sound_path):
        # st.warning(f"Sound file not found: {sound_path}") # Removed for cleaner output
        return

    try:
        with open(sound_path, "rb") as audio:
            b64 = base64.b64encode(audio.read()).decode("utf-8")
            components.html(f"""
                <audio autoplay loop controls style="display:none;">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """, height=0) # height=0 keeps the component from taking up space
    except Exception as e:
        # st.error(f"Error playing sound: {e}") # Removed for cleaner output
        pass # Fail silently for sound errors


# --- Main Application UI ---

# Custom Hero Header
st.markdown("<h1 class='app-title'>MAUSAM</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-subtitle'>Your daily atmospheric insights.</p>", unsafe_allow_html=True)

# City input with improved styling
city = st.text_input("Enter city name", placeholder="e.g., Lahore, New York, London", key="city_input") # Added a key

# --- Weather Data Fetching and Display ---
# Use a placeholder for the results that only gets filled when data is ready
results_placeholder = st.empty() # This will prevent the "weird empty bar" if it was a Streamlit artifact

if city:
    with st.spinner("Fetching weather data..."): # Show a spinner while fetching
        weather = get_weather_data(city)

    if weather:
        with results_placeholder.container(): # Fill the placeholder with content
            # --- Weather Result Card (the "pop-up" style section) ---
            st.markdown('<div class="weather-card">', unsafe_allow_html=True) # Start of the card

            # Card Header
            st.markdown(f"<h3 class='weather-card-header'>📍 Weather in {weather['city']}, {weather['country']}</h3>", unsafe_allow_html=True)

            # Main Temperature Display
            st.markdown(f"<p class='main-temp'>{weather['temp']}°C</p>", unsafe_allow_html=True)

            # Weather Parameters (arranged in a grid/columns)
            # Using st.columns for better alignment, then applying custom CSS
            col1, col2 = st.columns([1, 1]) # Equal width columns

            with col1:
                st.markdown(f"<div class='weather-param'><span class='icon'>🌤️</span> Condition:</div><p class='param-value'>{weather['condition']}</p>", unsafe_allow_html=True)
                st.markdown(f"<div class='weather-param'><span class='icon'>💧</span> Humidity:</div><p class='param-value'>{weather['humidity']}%</p>", unsafe_allow_html=True)

            with col2:
                st.markdown(f"<div class='weather-param'><span class='icon'>🌬️</span> Wind:</div><p class='param-value'>{weather['wind_kph']} kph</p>", unsafe_allow_html=True)
                st.markdown(f"<div class='weather-param'><span class='icon'>☁️</span> Cloud Cover:</div><p class='param-value'>{weather.get('cloud', 'N/A')}%</p>", unsafe_allow_html=True) # Added cloud cover, assuming it exists or default

            st.markdown('</div>', unsafe_allow_html=True) # End of the card


            # --- Dynamic Mood Quote ---
            quotes = {
                'rain': "☔ Perfect weather for chai and pakoras. Stay cozy!",
                'clear': "🌞 The sky is clear, and the day is bright. Enjoy!",
                'cloud': "☁️ Nice and cozy under the clouds. Perfect for contemplation.",
                'wind': "🍃 Hold onto your hat – it's breezy out there!",
                'overcast': "☁️ Overcast skies, a gentle light for your day.",
                'mist': "🌫️ Mist in the air, a touch of mystery.",
                'snow': "❄️ Winter wonderland! Stay warm and enjoy the view."
            }

            # Find a matching quote
            found_quote = False
            for key, quote_text in quotes.items():
                if key in weather['condition'].lower():
                    st.markdown(f'<p class="mood-quote">{quote_text}</p>', unsafe_allow_html=True)
                    found_quote = True
                    break
            if not found_quote:
                 st.markdown(f"<p class='mood-quote'>A unique day ahead!</p>", unsafe_allow_html=True) # CORRECTED LINE 115

            # --- Background Sound based on condition ---
            sound_file = None
            if "rain" in weather['condition'].lower():
                sound_file = "assets/rainy.mp3"
            elif "clear" in weather['condition'].lower():
                sound_file = "assets/sunny.mp3"
            elif "wind" in weather['condition'].lower():
                sound_file = "assets/breezy.mp3"
            elif "cloud" in weather['condition'].lower() or "overcast" in weather['condition'].lower():
                 sound_file = "assets/cloudy.mp3" # Assume you have this or similar

            if sound_file:
                play_background_sound(sound_file)

    else:
        results_placeholder.error("City not found or error fetching data. Please check the spelling or try another city.")

# --- Credit Footer ---
st.markdown('<p style="text-align: center; color: rgba(255, 255, 255, 0.4); font-size: 0.85rem; margin-top: 3rem;">Designed and Developed By Zain</p>', unsafe_allow_html=True)