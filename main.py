import streamlit as st
import requests
from weather.get_city_local_time import get_city_local_time_API, get_city_local_time_JSON
from weather.json_utils import load_json

st.title("Weather App")
name = st.text_input("Enter your name:")
if name:
    st.write(f"Hello {name}, welcome to the weather app")
    user_city = st.text_input("From which city are you using the app?").lower()
    if user_city:
        user_city_data = load_json('data/cities_timezone.json')
        if user_city in user_city_data:
            timezone = user_city_data[user_city]

            user_local_time, user_UTC_offset = get_city_local_time_JSON(timezone)
            st.write(f"{user_city} local time: {user_local_time}. {user_UTC_offset}.")
        #user_local_time, user_UTC_offset = get_city_local_time_API(user_city)
        #st.write(f"{user_city} local time: {user_local_time}. {user_UTC_offset}.")

    city = st.text_input("At which city you wish to check the current weather?").lower()
    if city:
        city_local_time, city_UTC_offset = get_city_local_time_API(city)
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
                st.write(f"Here's the current weather in {city}:")
                st.write(f"Data is updated to {data['location']['localtime']} local time.")
                st.write(f"Temperature is {data['current']['temp_c']} celsius degrees.")
                st.write(f"Humidity is {data['current']['humidity']}.")
                st.write(f"Wind speed is {data['current']['wind_kph']} kph.")
                col1, col2 = st.columns([1,3])
                with col1:
                    st.write(f"Conditions are: {data['current']['condition']['text']}.")
                with col2:
                    st.image(icon_url)
            else:
                st.write("Failed to fetch current weather. Try again later.")