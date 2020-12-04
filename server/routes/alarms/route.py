"""
This module handles all the api routing for this server.
"""
import os
import datetime

from flask import request, render_template

from server import app
from .alarm_scheduler import cancel_alarm, schedule_alarm, get_alarms
from .notification import get_notifications, remove_notification


# The format the date string from input[type="datetime-local"] is in
__DATE_FORMAT = "%Y-%m-%dT%H:%M"


@app.route("/")
@app.route("/index")
def render_interface():
    """
    Renders the main alarm interface using the template specified in config.interface_template
    """

    # the title of the alarm to be removed
    deleted_alarm_title = request.args.get("alarm_item", default="")
    # the title of the notification to be removed
    notification_title = request.args.get("notif", default="")
    # the time when an alarm will be scheduled
    new_alarm_time = request.args.get("alarm", default="")
    # the title of the alarm
    new_alarm_title = request.args.get("two", default="")
    # whether to include news briefing when the alarm fires
    include_news = request.args.get("news", default="")
    # whether to include weather briefing when the alarm fires
    include_weather = request.args.get("weather", default="")

    if notification_title:
        # the notif param is passed
        # delete the given notification
        remove_notification(notification_title)
        notifications = get_notifications(refresh=False)
    else:
        # refresh the list of notifications when the alarm title is not present
        # because we dont want to fetch news when the user is trying to remove alarms
        notifications = get_notifications(refresh=not deleted_alarm_title)

    if deleted_alarm_title:
        # the alarm_item param is passed
        # delete the given alarm
        cancel_alarm(deleted_alarm_title)

    alarms = get_alarms()

    if new_alarm_time and new_alarm_title:
        # the user wants to schedule an alarm
        schedule_alarm(
            title=new_alarm_title,
            at_time=datetime.datetime.strptime(new_alarm_time, __DATE_FORMAT),
            should_include_news=include_news,
            should_include_weather=include_weather,
        )

    return render_template(
        os.environ["INTERFACE_TEMPLATE"],
        notifications=notifications,
        alarms=alarms,
        image="logo.gif",
    )
