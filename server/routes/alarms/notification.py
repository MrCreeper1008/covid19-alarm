"""
This module handles notifications
"""

import datetime
from typing import List, Dict, Set, Any, Tuple

from flask import Markup

from server.api.news import fetch_news_headlines, calculate_news_id
from server.api.weather import fetch_weather
from server.api.covid import fetch_covid_data

# stores a list of notifications of news headlines in the shape of
# {
#     "title": "title of the notification",
#     "content": "Content of the notification",
# }
__notifications: Dict[str, Dict[str, Any]] = {}

# the set of removed notifications. they will never show up again.
__removed_notifications: Set[str] = set()

__WEATHER_NOTIFICATION_ID = "weather"


def get_notifications(refresh: bool = True) -> List[Dict[str, str]]:
    """
    Get a list of notifications.

    :params refresh: Whether to get new news. If false, the existing notifications will be returned
    :returns: The list of notifications
    """

    if refresh:
        covid_notification_id, covid_notification = __create_covid_notification()
        weather_notification_id, weather_notification = __create_weather_notification()

        __notifications[covid_notification_id] = covid_notification
        __notifications[weather_notification_id] = weather_notification

        news_headlines = fetch_news_headlines(country="gb")

        for news_headline in news_headlines:
            news_title = news_headline["title"]
            news_description = news_headline["description"]

            news_id = calculate_news_id(title=news_title, description=news_description)

            if (
                not news_id
                or news_id in __notifications
                or news_id in __removed_notifications
            ):
                continue

            __notifications[news_id] = __create_notification(
                title=news_title, content=news_description
            )

    return __notifications.values()


def remove_notification(title: str = ""):
    """
    Remove a notification from the list given the title of the notification.

    :params title: The title of the notification to be deleted.
    """

    for notification_id, notification in __notifications.items():
        # find the notification dict with matching title
        if notification["title"] == title:
            __notifications.pop(notification_id)
            __removed_notifications.add(notification_id)

            break


def __create_notification(title: str, content: str) -> Dict[str, Any]:
    """
    Creates a notification "object" from the given title and content.

    :params title: The title of the notification.
    :params content: The content of the notification.
    :returns A dictionary representing a notification "object".
    """
    return {"title": title, "content": content}


def __create_covid_notification() -> Tuple[str, Dict[str, Any]]:
    """
    Generates a Covid19 notification containing latest information about the pandemic.

    :returns: A tuple, first item being the id of the notification,
    second being the notification itself.
    """
    _, last_updated_on, new_cases, total_cases, __, ___ = fetch_covid_data()

    covid_notification_id = __covid_notification_id(
        last_updated_on, new_cases, total_cases
    )

    return covid_notification_id, __create_notification(
        title="Covid19 Data",
        content=Markup(
            f"""Data last updated on: <strong>{last_updated_on}</strong> <br>
New cases: <strong>{new_cases}</strong> <br>
Total cases: <strong>{total_cases}</strong>"""
        ),
    )


def __create_weather_notification() -> Tuple[str, Dict[str, Any]]:
    """
    Generates a weather notification containing latest weather information

    :returns: A tuple, first item being the id of the notification,
    second being the notification itself.
    """
    weather = fetch_weather(lat=50.718410, long=-3.533899)

    return __WEATHER_NOTIFICATION_ID, __create_notification(
        title="Current weather",
        content=Markup(
            f"""Temperature: <strong>{weather["main"]["temp"]} °C</strong> <br>
Feels like: <strong>{weather["main"]["feels_like"]} °C</strong> <br>
Humidity: <strong>{weather["main"]["humidity"]}</strong>"""
        ),
    )


def __covid_notification_id(
    last_updated_on: datetime.datetime,
    new_case_number: int,
    total_case_number: int,
) -> str:
    """
    Generates a notification ID for covid notifications.

    :params last_updated_on: The date the covid data is last updated on
    :params new_case_number: Number of new covid cases according to the data
    :params total_case_number: Number of total covid cases according to the data
    :returns: A notification ID to identify the covid notification
    """
    return f"covid_{last_updated_on}_{new_case_number + total_case_number}"
