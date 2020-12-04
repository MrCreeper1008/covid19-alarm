import requests
import logging
from pytest_mock import mock, MockerFixture

from server.api.news import calculate_news_id, fetch_news_headlines, NEWS_API_URL

__MOCK_API_KEY = "api-key"

__MOCK_API_RESULT = {
    "articles": [
        {
            "source": {"id": 1, "name": "Motley Fool Australia"},
            "author": "Peter Stephens",
            "title": "Forget gold and Bitcoin. I’d follow Warren Buffett’s advice after the stock market crash",
            "description": "Warren Buffett’s strategy of buying high-quality shares at low prices after a stock market crash could lead to higher returns than gold or Bitcoin, in my view.\nThe post Forget gold and Bitcoin. I’d follow Warren Buffett’s advice after the stock market crash a…",
            "url": "https://www.fool.com.au/?p=539807",
            "urlToImage": "https://www.fool.com.au/wp-content/uploads/2019/10/Warren-Buffett-profile-16.9.jpg",
            "publishedAt": "2020-12-03T23:30:16Z",
            "content": "Warren Buffett has a long track record of using share price declines, such as those experienced during a stock market crash, to his advantage. He has often used deteriorating market prospects to buy … [+3387 chars]",
        },
        {
            "source": {"id": 2, "name": "Screen Rant"},
            "author": "Adam Swimmer",
            "title": "Twitter Android & iOS Two-Factor Authentication: How To Get Started - Screen Rant",
            "description": "Two-factor authentication allows Twitter app users to better secure their accounts and data by setting up a second layer of protection.",
            "url": "https://screenrant.com/twitter-android-ios-two-factor-authentication-getting-started-how/",
            "urlToImage": "https://static1.srcdn.com/wordpress/wp-content/uploads/2020/12/Twitter-with-padlock.jpg",
            "publishedAt": "2020-12-03T23:10:00Z",
            "content": "One way for Twitter users to protect themselves from a potential hack is through two-factor authentication. While the feature itself is nothing new, the social media service recently added the abilit… [+4502 chars]",
        },
    ]
}

__mock_country = "country"


def test_fetch_news_headlines(mocker: MockerFixture):
    mocker.patch(
        "os.environ",
        {"NEWS_API_KEY": __MOCK_API_KEY},
    )
    mocker.patch(
        "requests.get",
        return_value=mock.Mock(json=lambda: __MOCK_API_RESULT),
        autospec=True,
    )

    result = fetch_news_headlines(__mock_country)

    assert len(result) == 2

    # pylint: disable=no-member
    requests.get.assert_called_once_with(
        f"{NEWS_API_URL}/v2/top-headlines",
        {"country": __mock_country, "apiKey": __MOCK_API_KEY},
    )


def test_calculate_news_id(mocker: MockerFixture):
    mocker.patch(
        "logging.error",
        autospec=True,
    )

    test_id = calculate_news_id(
        title="tiTle",
        description="descriPtion",
    )

    assert test_id == hex(0x6C6)

    invalid = calculate_news_id(1, 1)

    # pylint: disable=no-member
    logging.error.assert_called_once_with(
        "ValueError encountered when trying to calculate idempotency id for a news headline. "
        "This indicates that title or description is not a string. "
        "NewsAPI may have changed, causing type errors. \n"
        "Supplied title: %s\n"
        "Supplied description: %s",
        1,
        1,
    )

    assert invalid is None
