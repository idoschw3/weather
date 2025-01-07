from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

def get_city_local_time_API(city_name):
    """

    Args:
         city_name: city input
    return:
    (city local time in format YYYY-MM-DD H:M, UTC offset)

    # makes use of API
    """
    try:
        geolocator = Nominatim(user_agent="idoschw3-weather (https://idoschw3-weather.streamlit.app)")

        location = geolocator.geocode(city_name, timeout=30)

        if not location:
            return None, f"Could not find the city: {city_name}"

        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)

        timezone = pytz.timezone(timezone_str)
        city_time = datetime.now(timezone)

        utc_offset = city_time.utcoffset()
        offset_hours = utc_offset.total_seconds() // 3600
        offset_minutes = (utc_offset.total_seconds() % 3600) // 60
        formatted_offset = f"UTC {'+' if offset_hours >= 0 else ''}{int(offset_hours):02}:{int(offset_minutes):02}"

        return city_time.strftime('%Y-%m-%d %H:%M'), formatted_offset

    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        return None, f"Geocoding service error: {str(e)}"
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"

def get_city_local_time_JSON(timezone_str):
    """

    Args:
         city_name: city input
    return:
    (city local time in format YYYY-MM-DD H:M, UTC offset)

    # makes use of JSON
    """
    timezone = pytz.timezone(timezone_str)
    city_time = datetime.now(timezone)

    utc_offset = city_time.utcoffset()
    offset_hours = utc_offset.total_seconds() // 3600
    offset_minutes = (utc_offset.total_seconds() % 3600) // 60
    formatted_offset = f"UTC {'+' if offset_hours >= 0 else ''}{int(offset_hours):02}:{int(offset_minutes):02}"

    return city_time.strftime('%Y-%m-%d %H:%M'), formatted_offset