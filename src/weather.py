from typing import Tuple
import requests

# initial attributes - we can widdle down to just the essentials as necessary
WEATHER_ATTRIBUTES = [
    'name', 'startTime', 'endTime', 'temperature', 'temperatureUnit',
    'probabilityOfPrecipitation', 'windSpeed', 'windDirection',
    'shortForecast', 'detailedForecast',
]
NWS_URL = "https://api.weather.gov/points"

def call_nws(lat_lon: Tuple[float, float], is_hourly: bool = True) -> dict:
    url = f"{NWS_URL}/{lat_lon[0]},{lat_lon[1]}"
    response = requests.get(url)
    if is_hourly:
        granularity = "forecastHourly"
        n_units = 24 * 7
    else:
        granularity = "forecast"
        n_units = 2 * 7
    sub_url = response.json()["properties"][granularity]
    sub_response = requests.get(sub_url)
    forecast = [{k: sub_response.json()["properties"]["periods"][unit_from_now][k] for k in WEATHER_ATTRIBUTES} for unit_from_now in range(n_units)]
    return {lat_lon: forecast}


