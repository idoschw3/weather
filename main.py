import streamlit as st
import requests
from weather.get_city_local_time import get_city_local_time_api, get_city_local_time_json
from weather.json_utils import load_json
from weather.foliumm_utils import get_lat_lon, display_map
import json
import tempfile

st.title("Weather App")

# Initialize session_state if not present
if "reset" not in st.session_state:
    st.session_state.reset = False
if "name" not in st.session_state:
    st.session_state.name = ""
if "user_city" not in st.session_state:
    st.session_state.user_city = ""
if "city" not in st.session_state:
    st.session_state.city = ""

with st.container():
    default_values = {"name" : "", "user_city" : "", "city" : ""}

    uploaded_file = st.file_uploader("Upload your settings file (JSON)", type="json")
    st.write("""
    Upload a .json file only, formatted as follows:\n
    {"name": "your_name", "user_city": "your_city", "city": "city_name"}\n
    Ensure all keys and string values are enclosed in double quotes, and there are no trailing commas.\n
    Once uploaded, click on "Restore to Defaults".\n
    at the bottom of the page you can save your changes to defaults and generate a download link to default_setting.json file.
    """)

    # When file is uploaded, update the default values
    if uploaded_file is not None:
        default_values = json.load(uploaded_file)

    # Use a form to handle updates when pressing Enter
    with st.form(key="input_form"):
        # Set initial values based on session_state or default_values
        name = default_values["name"] if st.session_state.reset else st.session_state.get("name", default_values["name"])
        user_city = default_values["user_city"] if st.session_state.reset else st.session_state.get("user_city", default_values["user_city"])
        city = default_values["city"] if st.session_state.reset else st.session_state.get("city", default_values["city"])

        # Input fields
        st.session_state.name = st.text_input("Enter your name:", value=name)
        st.session_state.user_city = st.text_input("From which city are you using the app?", value=user_city)
        st.session_state.city = st.text_input("At which city you wish to check the current weather?", value=city)

        # Submit button inside the form
        submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        # Once submitted, update session state
        st.session_state.name = st.session_state.name
        st.session_state.user_city = st.session_state.user_city
        st.session_state.city = st.session_state.city

    if st.button("Restore to Default"):
        st.session_state.reset = True
        # Reset values to default after clicking the button
        st.session_state.name = default_values["name"]
        st.session_state.user_city = default_values["user_city"]
        st.session_state.city = default_values["city"]
        st.rerun()
    else:
        st.session_state.reset = False

if st.session_state.name:
    st.write(f"Hello {st.session_state.name}, welcome to the weather app.")

    if st.session_state.user_city:
        user_city_data = load_json('data/cities_timezone.json')
        if st.session_state.user_city in user_city_data:
            timezone = user_city_data[st.session_state.user_city]
            user_local_time, user_UTC_offset = get_city_local_time_json(timezone)
            st.write(f"{st.session_state.user_city} local time: {user_local_time}. {user_UTC_offset}.")
        else:
            timezone, user_local_time, user_UTC_offset = get_city_local_time_api(st.session_state.user_city)
            if timezone:
                st.write(f"{st.session_state.user_city} local time: {user_local_time}. {user_UTC_offset}.")

    if st.session_state.city:
        city_data = load_json('data/cities_timezone.json')
        if st.session_state.city in city_data:
            timezone = city_data[st.session_state.city]
            city_local_time, city_UTC_offset = get_city_local_time_json(timezone)
            st.write(f"{st.session_state.city} local time: {city_local_time}. {city_UTC_offset}.")
        else:
            timezone, city_local_time, city_UTC_offset = get_city_local_time_api(st.session_state.city)
            if timezone:
                st.write(f"{st.session_state.city} local time: {city_local_time}. {city_UTC_offset}.")

    if st.button("Show Weather Data"):
        key = '63e9898f15bf448cbe4130843250501'
        url = "http://api.weatherapi.com/v1/current.json"
        parameters = {
            'key': key,
            'q': st.session_state.city
        }
        response = requests.get(url, parameters)
        if response.status_code == 200:
            data = response.json()
            icon_url = "https:" + data['current']['condition']['icon']
            lat, lon = get_lat_lon(st.session_state.city)

            col1, col2 = st.columns([3, 2])
            with col1:
                st.write(f"Here's the current weather in {st.session_state.city}:")
                st.write(f"Data is updated to {data['location']['localtime']} local time.")
                st.write(f"Temperature is {data['current']['temp_c']} Celsius.")
                st.write(f"Humidity is {data['current']['humidity']}.")
                st.write(f"Wind speed is {data['current']['wind_kph']} kph.")
                col3, col4 = st.columns([1, 3])
                with col3:
                    st.write(f"Conditions are: {data['current']['condition']['text']}.")
                with col4:
                    st.image(icon_url)
            with col2:
                map_obj = display_map(lat, lon)
        else:
            st.write("Failed to fetch current weather. Try again later.")

if st.button("Save to Defaults"):
    # Create a dictionary with the current settings
    default = {"name": name, "user_city": user_city, "city": city}

    # Convert the dictionary to a JSON string
    json_data = json.dumps(default, indent=4)

    # Create a temporary file with a specific name that will be available for download
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w') as temp_file:
        temp_file.write(json_data)
        temp_file_path = temp_file.name

    # Provide a download link to the user with the file name 'default_settings.json'
    with open(temp_file_path, "rb") as f:
        st.download_button(
            label="Download Default Settings",
            data=f,
            file_name="default_settings.json",  # User will save it as default_settings.json
            mime="application/json"
        )
    st.success("Default settings file generated and ready to download!")