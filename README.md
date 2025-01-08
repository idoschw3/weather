Weather Application

Welcome to the Weather Application, a tool designed to provide weather information and local time data for cities worldwide. You can access the live application here: https://idoschw3-weather.streamlit.app.

---

Features

- Get weather updates for any city.
- View the local time for cities worldwide.
- Interactive maps using Folium integration.
- User-friendly interface powered by Streamlit.

---

Installation

Prerequisites
To run the application locally, ensure you have Python installed and Poetry for managing dependencies. 

Installation Steps
1. Clone this repository.
2. Navigate to the project directory.
3. Install dependencies using Poetry:
   poetry install

4. Alternatively, you can install the required modules listed in requirements.txt:
   pip install -r requirements.txt

---

Modules

The application is built using the following core modules:
- fliumm_utils.py: Contains utility functions for working with Folium maps.
- get_city_local_time.py: Retrieves and formats the local time for a given city.
- json_utils.py: Handles JSON file operations for managing user defaults and configurations.

---

Required Dependencies

The project relies on the following Python modules (as listed in pyproject.toml and requirements.txt):

- streamlit>=1.41.1
- requests>=2.32.3
- timezonefinder>=6.5.7
- datetime>=5.5
- pytz>=2024.2
- geopy>=2.4.1
- folium>=0.19.4
- streamlit-folium>=0.24.0

---

Usage Instructions

1. **Run the Application Locally**
   - Execute the `main.py` file using Streamlit:
     ```bash
     streamlit run main.py
     ```
   - Follow the prompts to search for city weather, view local time, and interact with maps.

2. **Adding a Default Settings File**
   - Upload a `.json` file only, formatted as follows:
     ```json
     {
       "name": "your_name",
       "user_city": "your_city",
       "city": "city_name"
     }
     ```
   - Ensure all keys and string values are enclosed in double quotes, and there are no trailing commas.
   - Once uploaded, click on **"Restore to Defaults"**.
   - At the bottom of the page, you can save your changes to defaults and generate a download link to the `default_setting.json` file.---

Known Issues

- App rerun script with every change leading to slower load times. 
- Use of Nominatim to get cities location - require API requests which can lead to too many requests

---

Future Plans

- Resolving full reruns for faster upload times of the data.
- Expand to cities_timezone.json data base to reduce API calls with Nominatim
- Improve Error Handling: Enhance feedback for users when input is invalid or a city is not found.
- Additional Features:
  - Add support for saving multiple city preferences.
  - Display historical weather trends.

---

Contributing

Contributions are welcome! Feel free to fork this repository, make changes, and submit a pull request.

---

Support

If you encounter any issues or have feature suggestions, feel free to open an issue in the GitHub repository.
