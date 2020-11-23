"""
This module handles all the api routing for this server.
"""
from flask import request

from server import app
from server.http_response import (
    HTTP_BAD_REQUEST,
    ERRCODE_INVALID_PARAMETERS,
    http_success_response,
    http_error_response,
)
from server.utils.logger import log_api_call
from .alarm_scheduler import cancel_alarm, schedule_alarm
from .notification import daily_brief

@app.route("/")
def test():
    """
    A test api endpoint.
    """
    return "Hello world"


@app.route("/alarm", methods=["POST"])
def set_alarm() -> str:
    """
    Handle POST /alarm api call. This endpoint allows user to schedule an alarm.
    """
    params = request.form

    log_api_call("/alarm", "POST", params=params)

    alarm_id = schedule_alarm(at_time=int(params["time"]), callback=daily_brief)

    return http_success_response(
        {
            "alarm_id": alarm_id,
        }
    )


@app.route("/alarms/<id>", methods=["DELETE"])
def delete_alarm(alarm_id: str) -> str:
    """
    Handles DELETE /alarms/<id> api call. Allows user to remove a scheduled alarm.
    """
    log_api_call(f"/alarms/{alarm_id}", "DELETE", params=None)

    try:
        cancel_alarm(alarm_id)
        return http_success_response(payload=None)
    except ValueError:
        return (
            http_error_response(
                code=ERRCODE_INVALID_PARAMETERS, details="The alarm does not exist."
            ),
            HTTP_BAD_REQUEST,
        )
