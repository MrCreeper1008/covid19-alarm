"""
Test code for server.api.covid
"""

import datetime
from pytest_mock import mock, MockerFixture

from server.api.covid import (
    fetch_covid_data,
    __covid_api_client,
    __get_date,
    __get_new_cases_count,
    __get_cumulative_cases_count,
    __get_new_deaths_count,
    __get_cumulative_deaths_count,
)

__mock_data_point = {
    "date": "2020-07-28",
    "areaName": "test-area-name",
    "areaCode": "test-area-code",
    # new cases on the given date
    "newCasesByPublishDate": 1,
    # cumulative cases up until the given date
    "cumCasesByPublishDate": 2,
    # number of new deaths on the given date
    "newDeathsByDeathDate": 3,
    # cumulative number of deaths up until the given date
    "cumDeathsByDeathDate": 4,
}

__mock_api_result = {
    "data": [
        {
            "date": "2020-07-28",
            "areaName": "England",
            "areaCode": "E92000001",
            "newCasesByPublishDate": 547,
            "cumCasesByPublishDate": 259022,
            "newDeathsByDeathDate": None,
            "cumDeathsByDeathDate": None,
        },
        {
            "date": "2020-07-27",
            "areaName": "England",
            "areaCode": "E92000001",
            "newCasesByPublishDate": 616,
            "cumCasesByPublishDate": 258475,
            "newDeathsByDeathDate": 20,
            "cumDeathsByDeathDate": 41282,
        },
    ]
}

__mock_today = datetime.datetime.strptime("2020-07-28", "%Y-%m-%d").date()


def test_fetch_covid_data(mocker: MockerFixture):
    mocker.patch.object(
        __covid_api_client,
        "get_json",
        lambda: __mock_api_result,
    )
    mocker.patch("datetime.date", mock.Mock(today=lambda: __mock_today))

    result = fetch_covid_data()

    assert result[0]
    assert result[2] == 547
    assert result[3] == 259022
    assert result[4] == 20
    assert result[5] == 41282


def test_get_date():
    date = __get_date(__mock_data_point)
    empty = __get_date({})

    assert date == datetime.date(2020, 7, 28)
    assert empty is None


def test_get_new_cases_count():
    new_cases = __get_new_cases_count(__mock_data_point)
    empty = __get_new_cases_count({})

    assert new_cases == 1
    assert empty == 0


def test_get_cumulative_cases_count():
    cumulative_cases = __get_cumulative_cases_count(__mock_data_point)
    empty = __get_cumulative_cases_count({})

    assert cumulative_cases == 2
    assert empty == 0


def test_get_new_deaths_count():
    new_deaths = __get_new_deaths_count(__mock_data_point)
    empty = __get_new_deaths_count({})

    assert new_deaths == 3
    assert empty == 0


def test_get_cumulative_deaths_count():
    cumulative_deaths = __get_cumulative_deaths_count(__mock_data_point)
    empty = __get_cumulative_cases_count({})

    assert cumulative_deaths == 4
    assert empty == 0
