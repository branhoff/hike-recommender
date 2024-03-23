from typing import Any, Dict, List, Tuple
import requests

# initial attributes - we can widdle down to just the essentials as necessary
WEATHER_ATTRIBUTES = [
    'name', 'startTime', 'endTime', 'temperature', 'temperatureUnit',
    'probabilityOfPrecipitation', 'windSpeed', 'windDirection',
    'shortForecast', 'detailedForecast',
]
NWS_URL = "https://api.weather.gov/points"


def call_nws(lat_lon: Tuple[float, float], is_hourly: bool = False) -> Dict[Tuple[float, float], List[Dict[str, Any]]]:
    url = f"{NWS_URL}/{lat_lon[0]},{lat_lon[1]}"
    response = requests.get(url)
    if is_hourly:
        granularity = "forecastHourly"
        n_units = None
    else:
        granularity = "forecast"
        n_units = 2 * 7
    sub_url = response.json()["properties"][granularity]
    sub_response = requests.get(sub_url)
    n_units = n_units or len(sub_response.json()["properties"]["periods"])
    forecast = [{k: sub_response.json()["properties"]["periods"][unit_from_now][k] for k in WEATHER_ATTRIBUTES} for unit_from_now in range(n_units)]
    return {lat_lon: forecast}
