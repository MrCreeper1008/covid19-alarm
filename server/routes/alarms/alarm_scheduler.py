"""
This module handles alarm scheduling
"""

import logging
import sched
import time
from flask import Markup
from datetime import datetime
from threading import Thread
from typing import List, Dict, Any

from .daily_brief import daily_brief

__scheduler = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)

# A map of alarm titles to the cooresponding alarm info in the shape of
__alarm_info: Dict[str, Dict[str, Any]] = {}

# A map of alarm titles to the scheduled event of the alarm
__schedules: Dict[str, sched.Event] = {}


def get_alarms() -> List[Dict[str, Any]]:
    """
    Gets the current list of alarms.

    :returns: The current list of alarms
    """
    return __alarm_info.values()


def schedule_alarm(
    title: str,
    at_time: datetime,
    should_include_weather: bool = False,
    should_include_news: bool = False,
) -> List[Dict[str, Any]]:
    """
    Schedule an alarm to run at specified time

    :params title: The title of the alarm
    :params at_time: The time when the alarm will fire
    :params callback: The function the scheduler should run when the alarm fires
    :returns: The new list of alarms after this alarm is scheduled.
    :raises ValueError: The given alarm time (at_time) is in the past.
    """

    time_delay = at_time - datetime.now()

    if time_delay.total_seconds() < 0:
        raise ValueError(f"Invalid alarm time given. Received: {at_time}")

    if title not in __alarm_info:
        new_alarm = __alarm(
            title=title,
            scheduled_time=at_time,
            include_news=should_include_news,
            include_weather=should_include_weather,
        )
        __alarm_info[title] = new_alarm
        __schedules[title] = __scheduler.enterabs(
            at_time.timestamp(), 1, lambda: __trigger_alarm(new_alarm)
        )
    else:
        existing_alarm = __alarm_info[title]

        logging.error(
            """
            User is trying to schedule an alarm with the same title as the existing alarm.
            Given alarm title: %s
            Existing alarm: Scheduled at %s,
            """,
            title,
            existing_alarm["scheduled_time"],
        )

    return __alarm_info.values()


def __trigger_alarm(alarm_info: Dict[str, Any]):
    __alarm_info.pop(alarm_info["title"])
    daily_brief(alarm_info)


def cancel_alarm(alarm_title: str):
    """
    Cancels a scheduled alarm.

    :params alarm_title: The title of the alarm to be deleted
    :raises ValueError: The alarm title is not associated with any alarm,
    or the alarm is not scheduled.
    """
    if alarm_title not in __schedules:
        raise ValueError(
            f"The given id: {alarm_title} is not associated with any alarm."
        )

    canceled_alarm = __alarm_info.pop(alarm_title)

    __scheduler.cancel(__schedules.pop(alarm_title))
    logging.info(
        "Alarm titled %s scheduled on %s canceled.",
        alarm_title,
        canceled_alarm["scheduled_time"],
    )


def __run_schedules():
    """
    Keep polling the scheduler queue to see if there are any events queueing.
    """
    while True:
        __scheduler.run()


def __alarm(
    title: str,
    scheduled_time: datetime,
    include_news: bool = False,
    include_weather: bool = False,
) -> Dict[str, Any]:
    """
    Creates a dictionary holding alarm information in the shape of:
    {
        "title": "Title of the alarm",
        "content": the time when the alarm fires
        "include_news": whether to include news briefing when the alarm fires.
        "include_weather": whether to include weather briefing when the alarm fires.
    }

    :params title: The title of the alarm
    :params content: The time when the alarm will fire
    :returns: A dictionary holding an alarm
    """

    return {
        "title": title,
        "scheduled_time": scheduled_time,
        "content": Markup(
            f"""Scheduled at: <strong>{scheduled_time}</strong> <br>
News briefing: <strong>{'enabled' if include_news else 'disabled'}</strong> <br>
Weather briefing: <strong>{'enabled' if include_weather else 'disabled'}</strong>"""
        ),
        "include_news": include_news,
        "include_weather": include_weather,
    }


# start a scheduler polling thread
Thread(target=__run_schedules).start()
