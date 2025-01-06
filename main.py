import streamlit as st
import requests
from weather.get_city_local_time import get_city_local_time, get_system_local_time

st.title("Weather App")
name = st.text_input("Enter your name:")
if name:
    st.write(f"Hello {name}, welcome to the weather app")
    st.write(f"your local time: {get_system_local_time()}.")
    city = st.text_input("At which city you wish to check the current weather?")
    if city:
        st.write(f"{city} local time: {get_city_local_time(city)}.")
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
                st.write(f"Here's the current weather in {city}:")
                st.write(f"Data is updated to {data['location']['localtime']} local time.")
                st.write(f"Temperature is {data['current']['temp_c']} celsius degrees.")
                st.write(f"Humidity is {data['current']['humidity']}.")
                st.write(f"Wind speed is {data['current']['wind_kph']} kph.")
                st.write(f"Conditions are: {data['current']['condition']['text']}.")
            else:
                st.write("Failed to fetch current weather. Try again later.")