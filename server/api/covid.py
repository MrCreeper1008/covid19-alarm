"""
This module handles interaction with the uk-covid19 API.
"""

import datetime
from typing import Dict, Any, Tuple

from uk_covid19 import Cov19API

from server.utils.logger import log_exception

# A filter that shows only covid cases in England
__CASE_FILTER_ENGLAND = [
    "areaType=nation",
    "areaName=England",
]

# The shape of the data we want. The API will return an array of json objects of this shape.
__DATA_SHAPE = {
    # the date a data point is representing
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    # new cases on the given date
    "newCasesByPublishDate": "newCasesByPublishDate",
    # cumulative cases up until the given date
    "cumCasesByPublishDate": "cumCasesByPublishDate",
    # number of new deaths on the given date
    "newDeathsByDeathDate": "newDeathsByDeathDate",
    # cumulative number of deaths up until the given date
    "cumDeathsByDeathDate": "cumDeathsByDeathDate",
}

# The format of the date stored in a data point
__DATE_FORMAT = "%Y-%m-%d"

__covid_api_client = Cov19API(
    filters=__CASE_FILTER_ENGLAND,
    structure=__DATA_SHAPE,
)


def fetch_covid_data() -> Tuple[bool, int, int, int, int]:
    """
    Retrieves the latest Covid19 data from official uk-covid19 API represented in a Tuple.

    :returns: A tuple that represents the latest Covid19 data.
    The first item tells whether the data is the latest. For example, this will be false
    if today's data is not available from the API.
    The second item is the number of new cases of the latest available date
    (today if the latest data is available).
    The third item is the number of cumulative cases up until the latest available date.
    The fourth item is the number of new deaths on the latest available date.
    The fifth item is the cumulative number of deaths up until the latest available date.

    :raises Exception: An exception has occurred when querying the API.
    """
    current_date = datetime.date.today()

    try:
        data = __covid_api_client.get_json()["data"]
        latest_data = data[0]
        data_from_yesterday = data[1]
        data_date = __get_date(latest_data)
        is_latest = data_date == current_date

        return (
            is_latest,
            data_date,
            __get_new_cases_count(latest_data),
            # cumulative cases number won't be available on today's data point
            __get_cumulative_cases_count(latest_data),
            __get_new_deaths_count(data_from_yesterday),
            __get_cumulative_deaths_count(data_from_yesterday),
        )
    except Exception as api_exception:
        log_exception(method="daily_brief > __covid_brief", exception=api_exception)
        raise api_exception


def __get_date(data_json: Dict[str, Any]) -> datetime.datetime:
    """
    Returns the date of a given data point from the API. Parses the date string
    in the data json to a datetime object.
    """
    try:
        return datetime.datetime.strptime(data_json["date"], __DATE_FORMAT).date()
    except KeyError:
        return None


def __get_new_cases_count(data_json: Dict[str, Any]) -> int:
    """
    Returns the number of new cases stored in the given data point.
    """
    try:
        return data_json["newCasesByPublishDate"]
    except KeyError:
        return 0


def __get_cumulative_cases_count(data_json: Dict[str, Any]) -> int:
    """
    Returns the cumulative number of cases stored in the given data point.
    """
    try:
        return data_json["cumCasesByPublishDate"]
    except KeyError:
        return 0


def __get_new_deaths_count(data_json: Dict[str, Any]) -> int:
    """
    Returns the number of new deaths stored in the given data point.
    """
    try:
        return data_json["newDeathsByDeathDate"]
    except KeyError:
        return 0


def __get_cumulative_deaths_count(data_json: Dict[str, Any]) -> int:
    """
    Returns the cumulative number of cases stored in the given data point.
    """
    try:
        return data_json["cumDeathsByDeathDate"]
    except KeyError:
        return 0
