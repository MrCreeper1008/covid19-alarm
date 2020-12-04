import logging
from pytest_mock import mock, MockerFixture

from server.routes.alarms.daily_brief import (
    __speech_engine,
    __covid_brief,
    __weather_brief,
    __news_brief,
    daily_brief,
)

__MOCK_NOW_TIME = "now"

__MOCK_ALARM_ALL_ENABLED = {
    "title": "test alarm",
    "include_news": True,
    "include_weather": True,
}


def test_daily_brief(mocker: MockerFixture):
    mocker.patch("datetime.datetime", mock.Mock(now=lambda: __MOCK_NOW_TIME))
    mocker.patch("logging.info", autospec=True)
    mocker.patch(
        "server.routes.alarms.daily_brief.__covid_brief",
        lambda: "covid brief",
    )
    mocker.patch(
        "server.routes.alarms.daily_brief.__weather_brief",
        lambda: "weather brief",
    )
    mocker.patch(
        "server.routes.alarms.daily_brief.__news_brief",
        lambda: "news brief",
    )
    mocker.patch.object(
        __speech_engine,
        'say',
        autospec=True
    )
    mocker.patch.object(
        __speech_engine,
        'runAndWait',
        autospec=True
    )

    expected_brief_message = f"""
    Hello! This is a scheduled daily brief titled: {__MOCK_ALARM_ALL_ENABLED["title"]}.
    covid brief
    weather brief
    news brief
    This is the end of your briefing. Have a nice day.
    """

    daily_brief(__MOCK_ALARM_ALL_ENABLED)

    # pylint: disable=no-member
    __speech_engine.say.assert_called_once_with(expected_brief_message)
    __speech_engine.runAndWait.assert_called_once()
