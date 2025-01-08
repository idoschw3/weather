import streamlit as st
import requests
from weather.get_city_local_time import get_city_local_time_api, get_city_local_time_json
from weather.json_utils import load_json
from weather.foliumm_utils import get_lat_lon, display_map
import json

st.title("Weather App")

default_values = {"name" : "", "user_city" : "", "city" : ""}

uploaded_file = st.file_uploader("Upload your settings file (JSON)", type="json")
st.write("""
upload .json file only, formated as follows:\n
{"name": "your_name", "user_city": "your_city", "city": "city_name"}\n
Ensure all keys and string values are enclosed in double quotes, and there are no trailing commas.
""")
if uploaded_file is not None:
    default_values = json.load(uploaded_file)


name = st.text_input("Enter your name:", value=default_values["name"])
if name:
    st.write(f"Hello {name}, welcome to the weather app")
    user_city = st.text_input("From which city are you using the app?", value=default_values["user_city"]).lower()
    if user_city:
        user_city_data = load_json('data/cities_timezone.json')
        if user_city in user_city_data:
            timezone = user_city_data[user_city]

            user_local_time, user_UTC_offset = get_city_local_time_json(timezone)
            st.write(f"{user_city} local time: {user_local_time}. {user_UTC_offset}.")
        else:
            timezone, user_local_time, user_UTC_offset = get_city_local_time_api(user_city)
            if timezone:
                st.write(f"{user_city} local time: {user_local_time}. {user_UTC_offset}.")

    city = st.text_input("At which city you wish to check the current weather?", value=default_values["city"]).lower()
    if city:
        city_data = load_json('data/cities_timezone.json')
        if city in city_data:
            timezone = city_data[city]

            city_local_time, city_UTC_offset = get_city_local_time_json(timezone)
            st.write(f"{city} local time: {city_local_time}. {city_UTC_offset}.")
        else:
            timezone, city_local_time, city_UTC_offset = get_city_local_time_api(city)
            if timezone:
                st.write(f"{city} local time: {city_local_time}. {city_UTC_offset}.")

        if st.button("show weather data"):
            key = '63e9898f15bf448cbe4130843250501'
            url = "http://api.weatherapi.com/v1/current.json"
            parameters = {
                'key': key,
                'q': city
            }
            response = requests.get(url, parameters)
            if response.status_code == 200:
                data = response.json()
                icon_url = "https:" + data['current']['condition']['icon']
                lat, lon = get_lat_lon(city)


                col1, col2 = st.columns([3, 2])
                with col1:
                    st.write(f"Here's the current weather in {city}:")
                    st.write(f"Data is updated to {data['location']['localtime']} local time.")
                    st.write(f"Temperature is {data['current']['temp_c']} celsius degrees.")
                    st.write(f"Humidity is {data['current']['humidity']}.")
                    st.write(f"Wind speed is {data['current']['wind_kph']} kph.")
                    col3, col4 = st.columns([1,3])
                    with col3:
                        st.write(f"Conditions are: {data['current']['condition']['text']}.")
                    with col4:
                        st.image(icon_url)
                with col2:
                    map_obj = display_map(lat, lon)
            else:
                st.write("Failed to fetch current weather. Try again later.")