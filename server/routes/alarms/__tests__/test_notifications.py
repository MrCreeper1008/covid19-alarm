from pytest_mock import mock, MockerFixture

from server.routes.alarms.notification import (
    __create_notification,
    get_notifications,
    remove_notification,
)

__MOCK_NOTIFICATIONS = {
    "id1": {
        "title": "1",
        "content": "1",
    },
    "id2": {
        "title": "2",
        "content": "2",
    },
}

__MOCK_FETCHED_NEWS = [
    {
        "title": "1",
        "description": "1",
    },
    {
        "title": "3",
        "description": "3",
    },
]

__MOCK_WEATHER = {"main": {"temp": 12, "feels_like": 10, "humidity": 100}}

__MOCK_NOTIFICATIONS_REFRESHED = {
    "id1": {
        "title": "1",
        "content": "1",
    },
    "id3": {
        "title": "3",
        "content": "3",
    },
}


def test_get_notifications(mocker: MockerFixture):
    mocker.patch(
        "server.routes.alarms.notification.__notifications",
        __MOCK_NOTIFICATIONS,
    )

    notifications = get_notifications(refresh=False)

    assert len(notifications) == len(__MOCK_NOTIFICATIONS.values())


def test_get_refreshed_notifications(mocker: MockerFixture):
    mock_notifications = __MOCK_NOTIFICATIONS.copy()

    mock_weather_notification = {
        "title": "weather",
        "content": "test",
    }

    mock_covid_notification = {
        "title": "covid",
        "content": "test",
    }

    mocker.patch(
        "server.routes.alarms.notification.__notifications",
        mock_notifications,
    )

    mocker.patch(
        "server.routes.alarms.notification.fetch_news_headlines",
        lambda country: __MOCK_FETCHED_NEWS,
    )

    mocker.patch(
        "server.routes.alarms.notification.calculate_news_id",
        lambda title, description: f"id{title}",
    )

    mocker.patch(
        "server.routes.alarms.notification.__create_covid_notification",
        lambda: ("covid", mock_covid_notification),
    )

    mocker.patch(
        "server.routes.alarms.notification.__create_weather_notification",
        lambda: ("weather", mock_weather_notification),
    )

    mocker.patch(
        "server.routes.alarms.notification.fetch_weather",
        lambda lat, long: __MOCK_WEATHER,
    )

    refreshed_notifications = get_notifications(refresh=True)

    assert len(refreshed_notifications) == 5
    assert mock_notifications["covid"] == mock_covid_notification
    assert mock_notifications["weather"] == mock_weather_notification


def test_remove_notifications(mocker: MockerFixture):
    removed = set()

    mocker.patch(
        "server.routes.alarms.notification.__removed_notifications",
        removed,
    )

    mocker.patch(
        "server.routes.alarms.notification.__notifications",
        __MOCK_NOTIFICATIONS,
    )

    mocker.patch(
        "server.api.news.calculate_news_id", lambda title, description: f"id{title}"
    )

    title = "1"

    remove_notification(title)

    assert f"id{title}" not in __MOCK_NOTIFICATIONS
    assert len(removed) == 1


def test_create_notification():
    test_title = "test title"
    test_content = "test content"
    notification = __create_notification(
        title=test_title,
        content=test_content,
    )

    assert notification["title"] == test_title
    assert notification["content"] == test_content
