"""
Logic relating to getting notifications for the user
"""

import logging

import pyttsx3
from server.api.weather import fetch_weather
from server.api.news import fetch_news_headlines

__speech_engine = pyttsx3.init()


def daily_brief():
    """
    Gives the user a brief of the current weather, the top news, and the local covid infection rate.
    """

    logging.info("daily brief")

    weather = fetch_weather(lat=50.718410, long=-3.533899)
    news = fetch_news_headlines(country="gb")

    brief_message = f"""
    Currently in your location, expect {weather['weather'][0]['description']}.
    The temperature is {weather['main']['temp']}.
    """

    if len(news["articles"]) == 0:
        brief_message += "There are no top news for you right now."
    else:
        brief_message += (
            "Also, here are some top news headlines for you.\n"
            + "\n".join([f"{article['title']}; " for article in news["articles"]])
        )

    logging.info("brief message: %s", brief_message)
    __speech_engine.say(brief_message)
    __speech_engine.runAndWait()
