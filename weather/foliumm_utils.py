import folium
import streamlit_folium as st_folium
import time
from geopy.geocoders import Nominatim

def get_lat_lon(city_name):
    geolocator = Nominatim(user_agent="idoschw3-weather (https://idoschw3-weather.streamlit.app)")
    time.sleep(1)

    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def display_map(lat, lon):
    map_obj = folium.Map(location=[lat,lon], zoom_start=10)
    folium.Marker([lat, lon], tooltip="Weather Location").add_to(map_obj)
    return map_obj