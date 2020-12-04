import requests
from pytest_mock import mock, MockerFixture

from server.api.weather import OPEN_WEATHER_API_URL, fetch_weather

__MOCK_API_KEY = "api-key"

__MOCK_API_RESULT = {
    "coord": {"lon": -122.08, "lat": 37.39},
    "weather": [
        {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}
    ],
    "base": "stations",
    "main": {
        "temp": 282.55,
        "feels_like": 281.86,
        "temp_min": 280.37,
        "temp_max": 284.26,
        "pressure": 1023,
        "humidity": 100,
    },
    "visibility": 16093,
    "wind": {"speed": 1.5, "deg": 350},
    "clouds": {"all": 1},
    "dt": 1560350645,
    "sys": {
        "type": 1,
        "id": 5122,
        "message": 0.0139,
        "country": "US",
        "sunrise": 1560343627,
        "sunset": 1560396563,
    },
    "timezone": -25200,
    "id": 420006353,
    "name": "Mountain View",
    "cod": 200,
}


def test_fetch_weather(mocker: MockerFixture):
    mocker.patch(
        "requests.get",
        return_value=mock.Mock(json=lambda: __MOCK_API_RESULT),
        autospec=True,
    )

    mocker.patch(
        "os.environ",
        {"OPEN_WEATHER_API_KEY": __MOCK_API_KEY},
    )

    mock_lat = 0
    mock_long = 0
    expected_url = f"{OPEN_WEATHER_API_URL}/weather"
    expected_params = {
        "lat": mock_lat,
        "lon": mock_long,
        "appid": __MOCK_API_KEY,
        "units": "metric",
    }

    result = fetch_weather(mock_lat, mock_long)

    assert result == __MOCK_API_RESULT
    # pylint: disable=no-member
    requests.get.assert_called_once_with(
        expected_url,
        expected_params,
    )
