import logging
from flask import request
from server import app
from server.utils.logger import log_api_call
from .alarm_scheduler import schedule_alarm
from .notification import daily_brief

@app.route("/")
def test():
    return "Hello world"


@app.route("/alarm", methods=["POST"])
def set_alarm() -> str:
    params = request.form

    log_api_call("/alarm", "POST", params=params)

    alarm_id = schedule_alarm(at=int(params["time"]), callback=daily_brief)

    return alarm_id
