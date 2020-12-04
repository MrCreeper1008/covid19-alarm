"""
This module handles daily brief processing.
"""

import logging
import datetime
from typing import Dict, Any

import pyttsx3

from server.api.weather import fetch_weather
from server.api.news import fetch_news_headlines
from server.api.covid import fetch_covid_data

__speech_engine = pyttsx3.init()


def daily_brief(alarm_info: Dict[str, Any]):
    """
    Gives the user a brief of the current weather, the top news, and the local covid infection rate.
    """

    logging.info("Daily brief initiated on %s.", datetime.datetime.now())

    alarm_title = alarm_info["title"]

    brief_message = f"""
    Hello! This is a scheduled daily brief titled: {alarm_title}.
    {__covid_brief()}
    {__weather_brief() if alarm_info["include_weather"] else ""}
    {__news_brief() if alarm_info["include_news"] else ""}
    This is the end of your briefing. Have a nice day.
    """

    logging.info("brief message: %s", brief_message)
    __speech_engine.say(brief_message)
    __speech_engine.runAndWait()


def __covid_brief() -> str:
    """
    Generates a brief message about the latest covid19 data.
    """

    try:
        (
            is_latest_covid_data_available,
            _,
            new_cases,
            cumulative_cases,
            new_deaths,
            cumulative_deaths,
        ) = fetch_covid_data()

        return f"""
        First, some Covid-19 update.
        {'Today, ' if is_latest_covid_data_available else 'Latest data is not available, so previous data will be recapped.'}
        In England, there are {new_cases} number of new cases,
        and unfortunately {new_deaths} people lost their battle against Covid19.
        In total, there are {cumulative_cases} number of cases,
        and {cumulative_deaths} lives are lost in this pandemic.
        """
    except:
        return "Unfortunately an error occurred when getting latest covid data."


def __weather_brief() -> str:
    """
    Generates a brief message about the current weather.
    """

    weather = fetch_weather(lat=50.718410, long=-3.533899)

    return f"""
    Currently in your location, expect {weather['weather'][0]['description']}.
    The temperature is {weather['main']['temp']}.
    """


def __news_brief() -> str:
    """
    Generates a brief message of latest news headlines.
    """

    news = fetch_news_headlines(country="gb")

    if len(news) == 0:
        return "There are no top news for you right now."

    return "Also, here are some top news headlines for you.\n" + "\n".join(
        [f"{article['title']}; " for article in news]
    )
