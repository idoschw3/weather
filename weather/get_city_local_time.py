from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

def get_city_local_time(city_name):
    try:
        geolocator = Nominatim(user_agent="idoschw3-weather (https://idoschw3-weather.streamlit.app)")

        location = geolocator.geocode(city_name, timeout=30)

        if not location:
            return None, f"Could not find the city: {city_name}"

        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)

        timezone = pytz.timezone(timezone_str)
        city_time = datetime.now(timezone)
        return city_time.strftime('%Y-%m-%d %H:%M')

    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        return None, f"Geocoding service error: {str(e)}"
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"