"""
This module handles interactions with NewsAPI
"""

import logging
import os
from typing import List, Dict

import requests

NEWS_API_URL = "https://newsapi.org"


def fetch_news_headlines(country: str) -> List[Dict[str, any]]:
    """
    Fetches top news headlines of the given country from newsapi.org.
    newsapi docs: https://newsapi.org/docs/endpoints/top-headlines

    :params country: The 2-letter ISO 3166-1 code of country the user is in.
    The list of codes are available in the docs linked above.
    :returns A list of dictionaries of information of a news headline
    """
    req_params = {"country": country, "apiKey": os.environ["NEWS_API_KEY"]}

    try:
        response = requests.get(f"{NEWS_API_URL}/v2/top-headlines", params=req_params)
        return response.json()
    except requests.ConnectionError as conn_err:
        logging.error(conn_err.strerror)
