"""
This module handles notifications
"""

import logging
from typing import List, Dict, Set

import pyttsx3
from server.api.weather import fetch_weather
from server.api.news import fetch_news_headlines, calculate_news_id

__speech_engine = pyttsx3.init()

# stores a list of notifications of news headlines in the shape of
# {
#     "title": "title of the notification",
#     "content": "Content of the notification",
# }
__notifications: List[Dict[str, str]] = []

# stores a list of ids of news that have been displayed to the user as notifications,
# calculated by the api.news.calculate_news_id function.
__old_news: Set[int] = set()


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


def get_notifications() -> List[Dict[str, str]]:
    """
    Get a list of notifications
    """
    notifications: List[Dict[str, str]] = []
    news_headlines = fetch_news_headlines(country="gb")

    for news_headline in news_headlines:
        news_title = news_headline["title"]
        news_description = news_headline["description"]

        print(news_title, news_description)

        news_id = calculate_news_id(title=news_title, description=news_description)

        if not news_id or news_id in __old_news:
            continue

        __old_news.add(news_id)
        notifications.append(
            __create_notification(title=news_title, content=news_description)
        )

    return notifications


def remove_notification(title: str = ""):
    """
    Remove a notification from the list given the title of the notification.

    :params title: The title of the notification to be deleted.
    """

    for notification in enumerate(__notifications):
        if notification["title"] == title:
            __notifications.remove(notification)
            break


def __create_notification(title: str, content: str) -> Dict[str, str]:
    """
    Creates a notification "object" from the given title and content.

    :params title: The title of the notification.
    :params content: The content of the notification.
    :returns A dictionary representing a notification "object".
    """
    return {"title": title, "content": content}
