import sched
import time
import uuid
from datetime import datetime
from threading import Thread
from typing import Dict

__scheduler = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)
__schedules: Dict[str, sched.Event] = {}


def schedule_alarm(at: int, callback: callable) -> str:
    """
    Schedule an alarm to run at specified time

    :params at: When the alarm should run in utc utx timestamp.
    """
    id = str(uuid.uuid4())

    __schedules[id] = __scheduler.enterabs(float(at), 1, callback)

    return id


def cancel_alarm(id: str):
    """
    Cancels a scheduled alarm.

    :params id: The id of the alarm to be canceled.
    :raises ValueError: Raises ValueError when the ID is not associated with any alarm, or when the alarm is not scheduled.
    """
    if id not in __schedules:
        raise ValueError(f"The given id: {id} is not associated with any alarm.")

    __scheduler.cancel(__schedules.pop(id))


def __run_schedules():
    """
    Keep polling the scheduler queue to see if there are any events queueing.
    """
    while True:
        __scheduler.run()


# start a scheduler polling thread
Thread(target=__run_schedules).start()
