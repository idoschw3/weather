import folium
import time
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static


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
    folium.Marker([lat, lon], popup="Requested Location").add_to(map_obj)
    st_data = folium_static(map_obj, width=400, height=400)
    return st_data