"""
This module handles interactions with NewsAPI
"""

import logging
import os
from typing import List, Dict
from functools import reduce

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
        return response.json()["articles"]
    except requests.ConnectionError as conn_err:
        logging.error(conn_err.strerror)
        return []


def calculate_news_id(title: str = "", description: str = "") -> hex:
    """
    Calculate an idempotency ID of a piece of news, by taking and summing the unicode values
    of each character (in lower case if applicable) in title and description
    and representing the final value in hex.

    Example:
        assert calculate_news_id(
            title="example title",
            description="example description"
        ) == hex('0xcde')

    :params title: Title of the news headline.
    :params description: Description of the news headline.
    :returns The hexidecimal representation of the idempotency ID of the news headline,
    or None if ValueError is encountered.
    """

    try:
        return hex(
            reduce(
                lambda final, char: final + ord(char),
                (title or "" + description or "").lower(),
                0,
            )
        )
    except ValueError:
        logging.error(
            "ValueError encountered when trying to calculate idempotency id for a news headline. "
            "This indicates that title or description is not a string. "
            "NewsAPI may have changed, causing type errors. \n"
            "Supplied title: %s\n"
            "Supplied description: %s",
            title,
            description,
        )
        return None
