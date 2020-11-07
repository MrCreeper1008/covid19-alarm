import requests
import logging
import os
from typing import Dict

OPEN_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5"


def fetch_weather(lat: float, long: float) -> Dict[str, any]:
    """
    Fetches the current weather from the OpenWeather api.

    :param lat: The latitude of user location
    :param long: The longitude of user location
    :returns: A dictionary of information of the current weather, as described in the OpenWeather api doc
    """

    # the request parameters required for the api call
    req_params = {
        "lat": lat,
        "lon": long,
        "appid": os.environ["OPEN_WEATHER_API_KEY"],
        "units": "metric",
    }

    try:
        response = requests.get(f"{OPEN_WEATHER_API_URL}/weather", params=req_params)
        return response.json()
    except requests.ConnectionError as req:
        logging.error(req.strerror)
