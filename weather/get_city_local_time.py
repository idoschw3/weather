from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

def get_city_local_time(city_name):
    try:
        geolocator = Nominatim(user_agent="idoschw3-weather (https://idoschw3-weather.streamlit.app)")
        location = geolocator.geocode(city_name, timeout=30)
        print(location)
        if not location:
            return None, f"Could not find the city: {city_name}"

get_city_local_time('Beer Sheva')